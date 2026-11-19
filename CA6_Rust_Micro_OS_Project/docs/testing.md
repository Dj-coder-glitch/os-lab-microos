# Testing and Evidence

## Automated Tests

Run native mechanism tests:

```powershell
cargo test
```

The integration suite validates:

- two-task Round Robin fairness;
- task termination state;
- timer quantum boundary;
- aligned allocation;
- allocation failure;
- spinlock-protected mutation;
- page replacement Belady's Anomaly and LRU stack algorithm invariance.

Build and boot the actual kernel:

```powershell
cargo build
.\scripts\run_qemu.ps1
```

The QEMU serial trace validates:

- BIOS bootloader handoff to the Rust kernel (`0x100000041a0`);
- serial console initialization (UART 16550 @ `0x3F8`);
- IDT, PIC, and PIT timer initialization;
- ASUS Vivobook 15 hardware adaptation;
- MediaTek Wi-Fi 6 MT7921 and Gigabit LAN link status;
- Aptitude / APT in-memory database and Snapstore daemon;
- timer-triggered scheduler decisions;
- task completion and queue exhaustion;
- kernel bump allocation;
- protected shared counter updates.

## Demonstration Evidence

Run the native demonstration:

```powershell
cargo run --bin micro-os-demo | Tee-Object traces/demo.log
```

The trace provides evidence for:

- kernel entry;
- subsystem initialization;
- task creation;
- timer ticks;
- scheduler order;
- task termination;
- synchronized shared counter updates;
- memory allocation;
- page replacement FIFO, LRU, and OPT execution with Belady anomaly detection;
- final switch and completion counts.

Capture the real boot trace with:

```powershell
.\scripts\run_qemu.ps1 | Tee-Object traces\qemu-boot.log
python scripts\analyze_trace.py traces\qemu-boot.log
```

## Required Experiment Matrix

| Case | Expected Observation |
| --- | --- |
| Two tasks | Alternating task selection until both terminate |
| Three tasks | Each ready task receives repeated turns |
| Short task | It terminates and leaves the queue |
| Large task | It remains ready across multiple turns |
| Invalid allocation | Request is rejected without changing allocator state |
| Belady test string | FIFO increases faults from 9 to 10; LRU decreases from 10 to 8 |
| Repeated run | Same deterministic task order and completion counts |

## Report Metrics

Record task switches, completion order, timer ticks, allocation usage, page replacement fault percentages, and final shared-counter value.
