import csv
import pandas as pd
from functools import reduce


#input below
ranked_fighters = {'Germaine de Randamie': {'Rank': 17}, 'Aspen Ladd': {'Rank': 3}, 'Urijah Faber': {'Rank': 23}, 'Ricky Simon': {'Rank': 2}, 'Josh Emmett': {'Rank': 19}, 'Mirsad Bektic': {'Rank': 5}, 'Karl Roberson': {'Rank': 6}, 'Wellington Turman': {'Rank': 22}, 'Cezar Ferreira': {'Rank': 20}, 'Marvin Vettori': {'Rank': 7}, 'Michael Rodriguez': {'Rank': 1}, 'John Allan': {'Rank': 24}, 'Andre Fili': {'Rank': 13}, 'Sheymon Moraes': {'Rank': 18}, 'Julianna Pena': {'Rank': 4}, 'Nicco Montano': {'Rank': 15}, 'Darren Elkins': {'Rank': 11}, 'Ryan Hall': {'Rank': 9}, 'Liu Pingyuan': {'Rank': 8}, 'Jonathan Martinez': {'Rank': 21}, 'Livinha Souza': {'Rank': 10}, 'Brianna Van Buren': {'Rank': 16}, 'Benito Lopez': {'Rank': 14}, 'Vince Morales': {'Rank': 12}}



all_combinations = [row for row in csv.reader(open("C:/Users/micha/Desktop/Python/Diversification_data.csv", "r"))]
all_combinations.sort(key=lambda row: row[-1], reverse=True)
top_combinations = []
next_rank = 1
worst_rank = reduce(
    lambda fighter_a, fighter_b: fighter_a
    if fighter_a["Rank"] > fighter_b["Rank"]
    else fighter_b,
    ranked_fighters.values(),
)["Rank"]
rank_counts = [0] * worst_rank
recent_ranks = [-1] * 3


for _ in range(150):
    recent_ranks.pop(0)
    recent_ranks.append(next_rank)
    for index, combination in zip(range(len(all_combinations)), all_combinations):
                # Don't use the current combination if any rank has more than 8 fighters
        if True and not any(map(lambda fighter: rank_counts[ranked_fighters[fighter]["Rank"] - 1] >= 86, combination[:6])): #Change ">=" int, switch and to or to have no player limit
            # Don't use the current combination if it shares 5 fighters with an already chosen combination
            if not any(map(lambda lineup: len(set(combination[:6]) & set(lineup[:6])) >= 5, top_combinations)):
                for fighter in combination[:6]:
                    if ranked_fighters[fighter]["Rank"] == next_rank:
                        print(f"Found match at {index:3} for rank {next_rank:2}: {fighter}")
                        # Count the fighters in the combination we found
                        for _fighter in combination[:6]:
                            rank_counts[ranked_fighters[_fighter]["Rank"] - 1] += 1
                            print(rank_counts)
                        top_combinations.append(all_combinations.pop(index))  # Add the combination we found
                        break  # Stop looking for next_rank
                else:
                    # This only happens when break isn't used
                    continue  # Current combination isn't invalid so skip back to the top of the loop
                break  # Current combination was valid so stop looping
    else:
        # This only happens when break isn't used
        print(
            f"No combination could be found for {next_rank}, changing worst rank and moving on"
        )
    ranks_check_next = [
        rank + 1
        for rank in range(worst_rank - 1)
        if rank + 1 not in recent_ranks and rank_counts[rank] <= rank_counts[rank + 1]
    ]
    next_rank = ranks_check_next[-1] if len(ranks_check_next) else worst_rank

print(len(top_combinations))

with open('test150_86_5_Event14.csv', 'w', newline='') as f:
    thewriter=csv.writer(f)
    thewriter.writerow(['Player 1','Player 2','Player 3','Player 4','Player 5','Player 6','Score'])
    for comb in top_combinations:
        thewriter.writerow(comb)