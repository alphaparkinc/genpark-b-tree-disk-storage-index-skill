from client import BPlusTreeIndex

def main():
    bpt = BPlusTreeIndex(order=4)
    for i in [10, 20, 5, 15, 25, 30]:
        bpt.insert(i, f"record_{i}")
    print("B+ Tree Index Verification:")
    print(f"Lookup key 15: {bpt.search(15)}")
    print(f"Range query [10, 25]: {bpt.range_query(10, 25)}")

if __name__ == "__main__":
    main()
