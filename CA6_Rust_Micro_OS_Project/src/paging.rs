//! Virtual Memory Page Replacement Simulation Engine
//! Implements FIFO, LRU, and Belady's Optimal (OPT) replacement algorithms
//! Based on Research Activity by Ved Raj (USN: 25BTRCL279)

pub fn fifo(refs: &[usize], num_frames: usize) -> usize {
    let mut frames = [None; 64];
    let mut faults = 0;
    let mut queue_head = 0;
    let mut frame_count = 0;

    for &page in refs {
        let mut hit = false;
        for i in 0..frame_count {
            if frames[i] == Some(page) {
                hit = true;
                break;
            }
        }
        if !hit {
            faults += 1;
            if frame_count < num_frames {
                frames[frame_count] = Some(page);
                frame_count += 1;
            } else {
                frames[queue_head] = Some(page);
                queue_head = (queue_head + 1) % num_frames;
            }
        }
    }
    faults
}

pub fn lru(refs: &[usize], num_frames: usize) -> usize {
    let mut frames = [None; 64];
    let mut last_used = [0usize; 64];
    let mut faults = 0;
    let mut frame_count = 0;

    for (step, &page) in refs.iter().enumerate() {
        let mut hit_idx = None;
        for i in 0..frame_count {
            if frames[i] == Some(page) {
                hit_idx = Some(i);
                break;
            }
        }

        if let Some(idx) = hit_idx {
            last_used[idx] = step;
        } else {
            faults += 1;
            if frame_count < num_frames {
                frames[frame_count] = Some(page);
                last_used[frame_count] = step;
                frame_count += 1;
            } else {
                // Find least recently used
                let mut lru_idx = 0;
                let mut min_step = last_used[0];
                for i in 1..num_frames {
                    if last_used[i] < min_step {
                        min_step = last_used[i];
                        lru_idx = i;
                    }
                }
                frames[lru_idx] = Some(page);
                last_used[lru_idx] = step;
            }
        }
    }
    faults
}

pub fn opt(refs: &[usize], num_frames: usize) -> usize {
    let mut frames = [None; 64];
    let mut faults = 0;
    let mut frame_count = 0;

    for (idx, &page) in refs.iter().enumerate() {
        let mut hit = false;
        for i in 0..frame_count {
            if frames[i] == Some(page) {
                hit = true;
                break;
            }
        }

        if !hit {
            faults += 1;
            if frame_count < num_frames {
                frames[frame_count] = Some(page);
                frame_count += 1;
            } else {
                // Find page whose next use is farthest in the future
                let mut victim_idx = 0;
                let mut farthest_next = 0;

                for i in 0..num_frames {
                    let resident_page = frames[i].unwrap();
                    let mut next_use = usize::MAX;
                    for j in (idx + 1)..refs.len() {
                        if refs[j] == resident_page {
                            next_use = j;
                            break;
                        }
                    }

                    if next_use > farthest_next {
                        farthest_next = next_use;
                        victim_idx = i;
                    }
                }
                frames[victim_idx] = Some(page);
            }
        }
    }
    faults
}

/// Checks Belady's Anomaly using the standard 12-reference sequence:
/// [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
/// Returns (faults_3_frames, faults_4_frames, anomaly_observed)
pub fn test_belady_anomaly() -> (usize, usize, bool) {
    let refs = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5];
    let f3 = fifo(&refs, 3);
    let f4 = fifo(&refs, 4);
    (f3, f4, f4 > f3)
}
