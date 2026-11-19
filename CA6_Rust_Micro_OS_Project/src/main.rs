use micro_os::kernel::Kernel;
use micro_os::paging::{fifo, lru, opt, test_belady_anomaly};

fn main() {
    println!("Micro-OS 2.0 educational microkernel demo (Ved Raj // USN: 25BTRCL279)");
    println!("[BOOT] Rust kernel entry reached");
    println!("[INIT] console, timer, scheduler, memory, network and paging ready");

    let mut kernel = Kernel::new();
    kernel.create_task(1, "shell", 3);
    kernel.create_task(2, "logger", 2);
    kernel.create_task(3, "worker", 4);

    println!("[TASK] created task 1: shell (3 steps)");
    println!("[TASK] created task 2: logger (2 steps)");
    println!("[TASK] created task 3: worker (4 steps)");

    while !kernel.scheduler.is_empty() {
        let quantum_expired = kernel.timer.tick();
        let event = kernel
            .scheduler
            .schedule_once()
            .expect("queue was not empty");
        let counter = kernel.increment_shared_counter();
        println!(
            "[SCHED] tick={} task={} ({}) quantum_expired={} shared_counter={} queue={:?}{}",
            kernel.timer.ticks,
            event.task_id,
            event.task_name,
            quantum_expired,
            counter,
            event.queue_after,
            if event.finished { " TERMINATED" } else { "" }
        );
    }

    let allocation = kernel
        .allocator
        .allocate(128, 8)
        .expect("demo allocation should fit");
    println!(
        "[MEM] allocated {} bytes at offset {}; used={}/{}",
        allocation.size,
        allocation.offset,
        kernel.allocator.used(),
        kernel.allocator.capacity()
    );

    // Page Replacement Research Activity Verification
    println!("[PAGING] testing Belady's Anomaly on reference string [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]");
    let (fifo_3, fifo_4, anomaly) = test_belady_anomaly();
    let lru_3 = lru(&[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 3);
    let lru_4 = lru(&[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 4);
    let opt_3 = opt(&[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 3);
    let opt_4 = opt(&[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 4);

    println!(
        "[PAGING] FIFO: 3 frames = {} faults, 4 frames = {} faults (Anomaly: {})",
        fifo_3, fifo_4, anomaly
    );
    println!(
        "[PAGING] LRU : 3 frames = {} faults, 4 frames = {} faults (Stack algo: preserved)",
        lru_3, lru_4
    );
    println!(
        "[PAGING] OPT : 3 frames = {} faults, 4 frames = {} faults (Theoretical minimum)",
        opt_3, opt_4
    );

    println!(
        "[DONE] switches={} completed_tasks={} final_counter={}",
        kernel.scheduler.switches,
        kernel.scheduler.completed,
        kernel.shared_counter()
    );
}
