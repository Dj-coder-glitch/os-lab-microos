use micro_os::memory::BumpAllocator;
use micro_os::paging::{fifo, lru, opt, test_belady_anomaly};
use micro_os::scheduler::RoundRobinScheduler;
use micro_os::sync::SpinLock;
use micro_os::task::{Task, TaskState};
use micro_os::timer::Timer;

#[test]
fn round_robin_is_fair_and_completes_tasks() {
    let mut scheduler = RoundRobinScheduler::new();
    scheduler.add_task(Task::new(1, "a", 2));
    scheduler.add_task(Task::new(2, "b", 2));

    let order: Vec<_> = (0..4)
        .map(|_| scheduler.schedule_once().unwrap().task_id)
        .collect();

    assert_eq!(order, vec![1, 2, 1, 2]);
    assert!(scheduler.is_empty());
    assert_eq!(scheduler.completed, 2);
}

#[test]
fn task_transitions_to_terminated() {
    let mut task = Task::new(7, "test", 1);
    assert_eq!(task.state, TaskState::Ready);
    assert!(task.run_one_step());
    assert_eq!(task.state, TaskState::Terminated);
}

#[test]
fn timer_expires_at_quantum_boundary() {
    let mut timer = Timer::new(3);
    assert!(!timer.tick());
    assert!(!timer.tick());
    assert!(timer.tick());
    assert_eq!(timer.ticks, 3);
}

#[test]
fn allocator_respects_alignment_and_failure() {
    let mut allocator = BumpAllocator::new(32);
    assert_eq!(allocator.allocate(3, 1).unwrap().offset, 0);
    assert_eq!(allocator.allocate(4, 8).unwrap().offset, 8);
    assert!(allocator.allocate(100, 8).is_none());
    assert!(allocator.allocate(2, 3).is_none());
}

#[test]
fn spinlock_protects_shared_value() {
    let lock = SpinLock::new(0usize);
    {
        let mut value = lock.lock();
        *value += 1;
    }
    assert_eq!(*lock.lock(), 1);
}

#[test]
fn page_replacement_belady_anomaly_and_stack_property() {
    let refs = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5];
    let (f3, f4, anomaly) = test_belady_anomaly();
    assert_eq!(f3, 9);
    assert_eq!(f4, 10);
    assert!(anomaly, "FIFO must exhibit Belady's Anomaly on this reference string");

    // Verify LRU is a stack algorithm (faults never increase with more frames)
    let lru_3 = lru(&refs, 3);
    let lru_4 = lru(&refs, 4);
    assert_eq!(lru_3, 10);
    assert_eq!(lru_4, 8);
    assert!(lru_4 <= lru_3, "LRU stack algorithm property violated");

    // Verify OPT benchmark
    let opt_3 = opt(&refs, 3);
    let opt_4 = opt(&refs, 4);
    assert_eq!(opt_3, 7);
    assert_eq!(opt_4, 6);
    assert!(opt_4 <= opt_3);
}
