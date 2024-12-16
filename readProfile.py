import pstats

def main():
    # Create a Stats object from the output.prof file
    p = pstats.Stats('output.prof')
    
    # Strip directory names from file paths
    p.strip_dirs()
    
    # Sort the statistics by cumulative time spent in the function
    p.sort_stats('cumulative')
    
    # Print the top 20 functions with the highest cumulative time
    p.print_stats(20)

if __name__ == "__main__":
    main()
