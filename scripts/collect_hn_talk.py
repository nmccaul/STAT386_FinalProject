from hiring_trends import hn


def main():
    counts = hn.talk_counts()
    print(f"Done. {len(counts)} months saved to {hn.RAW_DIR}/talk_counts.csv")


if __name__ == "__main__":
    main()
