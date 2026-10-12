

import math
import sys

# ------------------------------------------------------------------------------
# SYSTEM CONSTANTS & SLA THRESHOLDS
# ------------------------------------------------------------------------------
EXECUTION_RATE_OPS_PER_SEC = 1e8       # 10^8 basic operations per second (100 MHz)
SLA_MAX_TIME_SEC = 600.0               # Nightly batch SLA window: 10 minutes = 600s
SLA_MAX_OPERATIONS = SLA_MAX_TIME_SEC * EXECUTION_RATE_OPS_PER_SEC # 6.0e10 ops

# ------------------------------------------------------------------------------
# MODULE FORMULA DEFINITIONS (EXACT CLOSED-FORM EQUATIONS)
# ------------------------------------------------------------------------------

def ops_m1_duplicate_detector(n):
    """
    Module M1: Duplicate Detector - Pairwise Comparison Loop
    Asymptotic Bound: Theta(n^2)
    Exact Formula: C(n) = n * (n - 1) / 2
    """
    return n * (n - 1) // 2


def ops_m2_api_rate_limiter(n):
    """
    Module M2: API Rate Limiter - Segment Tree Audit Traversal
    Asymptotic Bound: Theta(n)
    Exact Formula: A(n) = 2^(floor(log2(n - 1)) + 1) - 1
    For power of 2 (e.g. n = 1024): A(1024) = 1023 audits.
    """
    if n <= 1:
        return 0
    exponent = math.floor(math.log2(n - 1)) + 1
    return (1 << exponent) - 1


def ops_s1_sequential_search(n, p=0.5):
    """
    Module S1: Sequential Search (Average Case with Target Hit Prob = p)
    Asymptotic Bound: Theta(n)
    Exact Formula: C_avg(n) = n - p*(n - 1)/2
    """
    return n - (p * (n - 1) / 2.0)


def ops_s2_binary_search(n):
    """
    Module S2: Product Catalog Search (Binary Search)
    Asymptotic Bound: Theta(log n)
    Exact Formula: C(n) = floor(log2(n)) + 1
    """
    if n <= 0:
        return 0
    return math.floor(math.log2(n)) + 1


def ops_m4_rec_engine_current(n):
    """
    Module M4: Recommendation Engine (Current - 4 Sub-partitions)
    Asymptotic Bound: Theta(n^2)
    Recurrence: T(n) = 4*T(n/2) + n
    Closed Form: T(n) = 2*n^2 - n
    """
    return 2 * (n ** 2) - n


def ops_m4_rec_engine_proposed(n):
    """
    Module M4: Recommendation Engine (Proposed Redesign - 2 Sub-partitions)
    Asymptotic Bound: Theta(n log n)
    Recurrence: T(n) = 2*T(n/2) + n
    Closed Form: T(n) = n * log2(n) + n
    """
    return n * math.log2(n) + n


def ops_m5_analytics_engine(n):
    """
    Module M5: Analytics Engine Pipeline
    Asymptotic Bound: Theta(n log^2 n)
    Recurrence: T(n) = 2*T(n/2) + n * log2(n)
    Closed Form: T(n) = 0.5 * n * (log2(n))^2 + 0.5 * n * log2(n)
    """
    log_n = math.log2(n)
    return 0.5 * n * (log_n ** 2) + 0.5 * n * log_n


def ops_m5_report_generator(n):
    """
    Module M5: Executive Report Generator
    Asymptotic Bound: Theta(n^2)
    Exact Formula: f(n) = 3*n^2 + 10*n*log2(n) + 50
    """
    return 3 * (n ** 2) + 10 * n * math.log2(n) + 50


# ------------------------------------------------------------------------------
# SMALL-SCALE VERIFICATION SIMULATOR (FUNCTIONS FOR REAL EXECUTION IN IDLE)
# ------------------------------------------------------------------------------

def simulate_m2_segment_tree(n):
    """
    Simulates the segment tree internal audit node count for a given n.
    An internal audit occurs at every non-leaf split node (where size > 1).
    """
    count = 0
    def traverse(size):
        nonlocal count
        if size > 1:
            count += 1
            half = size // 2
            traverse(half)
            traverse(size - half)
    traverse(n)
    return count


def verify_m2_formula():
    """Verifies M2 formula against simulation for n = 1024."""
    n_test = 1024
    simulated_count = simulate_m2_segment_tree(n_test)
    formula_count = ops_m2_api_rate_limiter(n_test)
    match = (simulated_count == formula_count)
    return n_test, simulated_count, formula_count, match


# ------------------------------------------------------------------------------
# ASCII VISUALIZATION GENERATOR (PURE TEXT BAR CHART FOR IDLE CONSOLE)
# ------------------------------------------------------------------------------

def render_ascii_scalability_chart(results_1m):
    """
    Generates a clean ASCII log-scale execution time chart directly in IDLE console.
    """
    print("\n" + "=" * 95)
    print("      VISUAL ARTIFACT: LOGARITHMIC EXECUTION TIME SCALE AT N = 1,000,000 PRODUCT ITEMS")
    print("=" * 95)
    print(f"SLA Cutoff Window: {SLA_MAX_TIME_SEC:.1f} Seconds (10.0 Minutes)")
    print("-" * 95)
    
    max_char_width = 40
    max_time_log = math.log10(30000.0) # max time ~ 30,000 seconds
    
    for module_name, ops, time_sec, status in results_1m:
        if time_sec > 0:
            time_log = math.log10(max(time_sec, 1e-7)) + 7 # Shift to positive scale
            bar_len = int((time_log / (max_time_log + 7)) * max_char_width)
            bar_len = max(1, min(bar_len, max_char_width))
        else:
            bar_len = 1
            
        bar_symbol = "█" if "FAIL" in status else "■"
        bar_str = bar_symbol * bar_len
        
        time_str = f"{time_sec:.4f}s" if time_sec >= 1.0 else (
            f"{time_sec*1000:.2f}ms" if time_sec >= 0.001 else f"{time_sec*1e6:.1f}µs"
        )
        print(f"{module_name:<28} | {bar_str:<40} | {time_str:>10} [{status}]")
        
    print("-" * 95)
    print("Legend: █ = Critical SLA Failure (>600s) | ■ = Healthy / Within SLA (<600s)")
    print("=" * 95 + "\n")


# ------------------------------------------------------------------------------
# MAIN AUDIT SUITE EXECUTION
# ------------------------------------------------------------------------------

def run_scalability_audit():
    print("=" * 95)
    print("                      SHOPSPHERE ALGORITHM SCALABILITY AUDIT REPORT")
    print("                      System Speed: 1.0e+08 ops/sec | SLA Limit: 600.0 sec")
    print("=" * 95)
    
    # Step 1: Verification of Module M2
    n_ver, sim_c, form_c, match = verify_m2_formula()
    print(f"\n[Verification] M2 Audit for N = {n_ver}:")
    print(f"  - Simulated Traversal Count : {sim_c}")
    print(f"  - Formula A(n) Result        : {form_c}")
    print(f"  - Exact Match Confirmed     : {match}\n")
    
    # Step 2: Define Modules to Audit
    modules = [
        ("M1: Duplicate Detector", ops_m1_duplicate_detector, "Theta(n^2)"),
        ("M2: API Rate Limiter", ops_m2_api_rate_limiter, "Theta(n)"),
        ("S1: Sequential Search (p=0.5)", ops_s1_sequential_search, "Theta(n)"),
        ("S2: Catalog Search (Binary)", ops_s2_binary_search, "Theta(log n)"),
        ("M4: Rec. Engine (Current)", ops_m4_rec_engine_current, "Theta(n^2)"),
        ("M4: Rec. Engine (Proposed)", ops_m4_rec_engine_proposed, "Theta(n log n)"),
        ("M5: Analytics Engine", ops_m5_analytics_engine, "Theta(n log^2 n)"),
        ("M5: Executive Report Gen.", ops_m5_report_generator, "Theta(n^2)")
    ]
    
    n_sizes = [100000, 1000000]
    
    # Table Header
    header = (
        f"{'Module Name':<28} | {'N = 100K Ops':<13} | {'Time (s)':<9} | "
        f"{'N = 1M Ops':<13} | {'Time (s)':<10} | {'SLA Status'}"
    )
    print("-" * 105)
    print(header)
    print("-" * 105)
    
    chart_data_1m = []
    
    for name, func, bound in modules:
        # N = 100,000
        ops_100k = func(n_sizes[0])
        time_100k = ops_100k / EXECUTION_RATE_OPS_PER_SEC
        
        # N = 1,000,000
        ops_1m = func(n_sizes[1])
        time_1m = ops_1m / EXECUTION_RATE_OPS_PER_SEC
        
        status = "FAIL (CRITICAL)" if time_1m > SLA_MAX_TIME_SEC else "PASS"
        chart_data_1m.append((name, ops_1m, time_1m, status))
        
        # Print row
        row = (
            f"{name:<28} | {ops_100k:<13.3e} | {time_100k:<9.3f} | "
            f"{ops_1m:<13.3e} | {time_1m:<10.3f} | {status}"
        )
        print(row)
        
    print("-" * 105)
    
    # Step 3: Render ASCII Visual Trajectory Chart
    render_ascii_scalability_chart(chart_data_1m)
    
    # Step 4: Summary Recommendations
    print("=" * 95)
    print("                          EXECUTIVE REDESIGN ROADMAP")
    print("=" * 95)
    print("1. M1 Duplicate Detector: Replace O(n^2) nested loop with Hash-based Indexing (O(n)).")
    print("2. M4 Recommendation Engine: Adopt Proposed Divide-and-Conquer Redesign (95,500x faster).")
    print("3. M5 Report Generator: Replace full O(n^2) scan with streaming incremental aggregates.")
    print("=" * 95 + "\n")

if __name__ == "__main__":
    run_scalability_audit()
