import math

# ------------------------------------------------------------------------------
# 1. CORRECTED FUNCTIONS (Fixing all 9 defects)
# ------------------------------------------------------------------------------

def sort_alerts(alerts):
    """Sorts alerts by severity descending (Insertion Sort). Fixes D1, D2, D3."""
    arr = list(alerts)
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j][1] < key[1]:  # j >= 0 includes index 0; < key[1] sorts highest severity first
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key                       # Assign to j + 1
    return arr

def is_blocked(blocklist, ip):
    """Checks if IP is blacklisted (Linear Search). Fixes D4, D5."""
    for item in blocklist:
        if item == ip:
            return True   # Returns True if found
    return False          # Returns False only after full search

def find_signature(log, pattern):
    """Finds pattern start indices in log (Brute Force). Fixes D6, D7."""
    n, m = len(log), len(pattern)
    hits = []
    if m == 0 or n < m:
        return hits
    for i in range(n - m + 1):  # Includes index n - m
        if log[i:i + m] == pattern:  # Checks full slice
            hits.append(i)
    return hits

def closest_logins(events):
    """Finds closest pair of coordinates (Brute Force). Fixes D8, D9."""
    if len(events) < 2:
        return None, float('inf')
    min_dist = float('inf')  # Initialized to infinity
    pair = None
    for i in range(len(events)):
        for j in range(i + 1, len(events)):  # Avoids self-loops and duplicate pairs
            dx = events[i][0] - events[j][0]
            dy = events[i][1] - events[j][1]
            d = math.sqrt(dx * dx + dy * dy)
            if d < min_dist:
                min_dist = d
                pair = (i, j)
    return pair, min_dist

# ------------------------------------------------------------------------------
# 2. OPTIMIZED FUNCTIONS (Production Scale)
# ------------------------------------------------------------------------------

def is_blocked_opt(blocklist_set, ip):
    """O(1) Hash Set Lookup."""
    return ip in blocklist_set

def find_signature_kmp(log, pattern):
    """Knuth-Morris-Pratt O(N+M) String Match."""
    n, m = len(log), len(pattern)
    if m == 0 or n < m:
        return []
    # Build LPS table
    lps = [0] * m
    prev, i = 0, 1
    while i < m:
        if pattern[i] == pattern[prev]:
            prev += 1; lps[i] = prev; i += 1
        elif prev != 0:
            prev = lps[prev - 1]
        else:
            lps[i] = 0; i += 1
    # Search
    hits, i, j = [], 0, 0
    while i < n:
        if log[i] == pattern[j]:
            i += 1; j += 1
        if j == m:
            hits.append(i - j)
            j = lps[j - 1]
        elif i < n and log[i] != pattern[j]:
            if j != 0: j = lps[j - 1]
            else: i += 1
    return hits

def closest_logins_opt(events):
    """O(N log N) Sweep-Line Closest Pair."""
    if len(events) < 2:
        return None, float('inf')
    pts = sorted((events[i][0], events[i][1], i) for i in range(len(events)))
    
    def dist_sq(p1, p2):
        return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

    min_sq = float('inf')
    best_pair = None
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if (pts[j][0] - pts[i][0])**2 >= min_sq:
                break  # Bounding box pruning
            d_sq = dist_sq(pts[i], pts[j])
            if d_sq < min_sq:
                min_sq = d_sq
                p_i, p_j = pts[i][2], pts[j][2]
                best_pair = (p_i, p_j) if p_i < p_j else (p_j, p_i)
    return best_pair, math.sqrt(min_sq)

# ------------------------------------------------------------------------------
# 3. TEST RUNNER (IDLE Compatible)
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    # Test Data
    alerts = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
    blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
    queries = ["10.0.0.9", "10.0.0.5", "8.8.8.8"]
    log, pattern = "FAILFAIXFAIL", "FAIL"
    events = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]

    print("=== CORRECTED RESULTS ===")
    print("Sorted Alerts:   ", sort_alerts(alerts))
    print("Blocklist Checks:", [is_blocked(blocklist, q) for q in queries])
    print("Signature Matches:", find_signature(log, pattern))
    pair, dist = closest_logins(events)
    print(f"Closest Logins:   Pair {pair}, Distance: {dist:.4f} km")

    print("\n=== OPTIMIZED RESULTS ===")
    print("O(1) HashSet Checks:", [is_blocked_opt(set(blocklist), q) for q in queries])
    print("KMP Pattern Matches:", find_signature_kmp(log, pattern))
    p_opt, d_opt = closest_logins_opt(events)
    print(f"Sweep-Line Logins:   Pair {p_opt}, Distance: {d_opt:.4f} km")
