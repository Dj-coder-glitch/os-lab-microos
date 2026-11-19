# Architecture

## Control Flow

```text
BIOS / UEFI El Torito Bootloader (Stage 1 -> Stage 2 -> Stage 3 -> Stage 4)
      |
      v
`kernel/src/main.rs` Rust `no_std` entry point
      |
      +--> UART 16550 Serial Console (0x3F8, 115200 Baud)
      |
      +--> Hardware Adaptation: ASUS Vivobook 15 (Intel Core i5-12500H)
      |
      +--> Dual Network Stack: MediaTek Wi-Fi 6 MT7921 + Gigabit LAN (smoltcp)
      |
      +--> Package Manager & App Store: Aptitude / APT + Snapstore (snapd loop)
      |
      +--> IDT + PIC + PIT Timer Interrupt (20 Hz) + PS/2 Keyboard IRQ 1
      |       |
      |       +--> Round Robin Ready Queue (Interactive Shell, Logger, Worker)
      |               |
      |               +--> Task: runs controlled work unit
      |
      +--> Virtual Memory Page Replacement Engine (`src/paging.rs`: FIFO, LRU, OPT)
      |
      +--> SpinLock: atomic Acquire/Release mutual exclusion
      |
      +--> Bump Allocator: 64 KiB monotonic power-of-two aligned heap
      |
      v
VESA Linear Framebuffer Desktop (800x600 24-bpp) & Serial Execution Trace
```

## Modules

| Module | Responsibility |
| --- | --- |
| Root `src/task.rs` | Host-test task identity, state, and work units |
| Root `src/scheduler.rs` | Host-test ready queue and Round Robin selection |
| Root `src/timer.rs` | Host-test tick count and quantum expiry |
| Root `src/sync.rs` | Host-test atomic spinlock and scoped guard |
| Root `src/memory.rs` | Host-test aligned bump allocation and failure handling |
| Root `src/paging.rs` | Host-test page replacement engine (FIFO, LRU, OPT & Belady Anomaly) |
| `kernel/src/main.rs` | Real no_std kernel, timer interrupt, PS/2 shell, network, APT, store, and VESA UI |
| `build.rs` | Builds the kernel artifact and synthesizes the El Torito hybrid ISO image |

## Scheduling Invariant

A task enters the ready queue only in `Ready` state. Each scheduling decision removes exactly one task. A task with remaining work returns to the back of the queue; a task with no remaining work becomes `Terminated` and is not requeued.

## Synchronization Invariant

Only the holder of a `SpinLockGuard` can access the protected value mutably. Dropping the guard releases the atomic lock with `Release` ordering.

## Memory Invariant

`next` always points to the first unused byte. Allocations are monotonic, aligned to a power-of-two boundary, and never exceed the heap capacity. This is intentionally a bump allocator: individual blocks are not freed.

## Page Replacement & Locality Invariant

LRU satisfies the stack algorithm inclusion property: for any reference sequence, the set of resident pages in $m$ frames is always a subset of the set in $m+1$ frames ($M(m) \subseteq M(m+1)$), guaranteeing freedom from Belady's Anomaly.
