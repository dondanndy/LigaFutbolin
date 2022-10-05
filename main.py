import numpy as np
import random

from typing import Union


PLAYER_NAMES = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


class Team:
    def __init__(self, p1: int, p2: int):
        self.players = [p1, p2]
        # shuffle(self.players)

    def __str__(self):
        return f"{PLAYER_NAMES[self.players[0]]}-{PLAYER_NAMES[self.players[1]]}"


class Match:
    def __init__(self, t1: Team, t2: Team):
        self.teams = [t1, t2]

    def __str__(self):
        return f"{self.teams[0]} vs. {self.teams[1]}"

    def includes_player(self, player):
        return player in self.teams[0].players or player in self.teams[1].players

    def get_player_pair(self, player):
        if player == self.teams[0].players[0]:
            return self.teams[0].players[1]

        if player == self.teams[0].players[1]:
            return self.teams[0].players[0]

        if player == self.teams[1].players[0]:
            return self.teams[1].players[1]

        if player == self.teams[1].players[1]:
            return self.teams[1].players[0]

        return None

    def get_player_opponents(self, player):
        if player in self.teams[0].players:
            return self.teams[1].players

        if player in self.teams[1].players:
            return self.teams[0].players

        return None

def init_prob_matrix(n: int):
  prob_matrix = np.ones((n,n))
  prob_matrix[np.diag_indices(n)] = 0

  return prob_matrix


def update_players_relationship_probability(matrix: np.array, update_factor: float, idx: int, idy: int) -> None:
    matrix[idx, idy] *= update_factor
    matrix[idy, idx] *= update_factor


def set_player_not_elegible(matrix: np.array, player: Union[int, np.array]) -> None:
  matrix[:, player] = 0


def normalize(prob: np.array) -> np.array:
  return prob/sum(prob)


# -----------------------------------------------
# INPUT PARAMETERS
# -----------------------------------------------

NUM_OF_PLAYERS = 20
MATCHDAYS = 10

TEAMMATE_PROBABILITY_DECREASE_FACTOR_AFTER_MATCH = 1/2
RIVAL_PROBABILITY_DECREASE_FACTOR_AFTER_MATCH = 1/3

# -----------------------------------------------
# DRAW
# -----------------------------------------------

NUM_OF_PLAYERS += NUM_OF_PLAYERS % 4  # Fill the missing players

num_games_per_matchday = NUM_OF_PLAYERS // 4

rivals_prob_matrix    = init_prob_matrix(NUM_OF_PLAYERS)
teammates_prob_matrix = init_prob_matrix(NUM_OF_PLAYERS)

players = np.arange(NUM_OF_PLAYERS)

matches = []

for _ in range(MATCHDAYS):
  matchday = []

  matchday_teammates_prob_matrix = teammates_prob_matrix.copy()
  matchday_rivals_prob_matrix    = rivals_prob_matrix.copy()

  first_player_chosen_for_each_match = np.random.choice(players, num_games_per_matchday, replace=False)

  # These players are already selected:
  set_player_not_elegible(matchday_teammates_prob_matrix, first_player_chosen_for_each_match)
  set_player_not_elegible(matchday_rivals_prob_matrix, first_player_chosen_for_each_match)

  for player in first_player_chosen_for_each_match:
    def select_player(player: int, selected_player_prob: np.array) -> int:
      selected_player = np.random.choice(players, 1, p=normalize(selected_player_prob))[0]

      set_player_not_elegible(matchday_rivals_prob_matrix, selected_player)
      set_player_not_elegible(matchday_teammates_prob_matrix, selected_player)

      return selected_player

    # Teammate
    teammates_prob = matchday_teammates_prob_matrix[player]
    teammate = select_player(player, teammates_prob)

    update_players_relationship_probability(teammates_prob_matrix, TEAMMATE_PROBABILITY_DECREASE_FACTOR_AFTER_MATCH, player, teammate)

    # Rival 1
    first_rival_prob = matchday_rivals_prob_matrix[player] * matchday_rivals_prob_matrix[teammate]
    rival1 = select_player(player, first_rival_prob)

    update_players_relationship_probability(rivals_prob_matrix, RIVAL_PROBABILITY_DECREASE_FACTOR_AFTER_MATCH, player, rival1)
    update_players_relationship_probability(rivals_prob_matrix, RIVAL_PROBABILITY_DECREASE_FACTOR_AFTER_MATCH, teammate, rival1)

    # Rival 2
    second_rival_prob = first_rival_prob * matchday_teammates_prob_matrix[rival1]
    rival2 = select_player(player, second_rival_prob)

    update_players_relationship_probability(rivals_prob_matrix, RIVAL_PROBABILITY_DECREASE_FACTOR_AFTER_MATCH, player, rival2)
    update_players_relationship_probability(rivals_prob_matrix, RIVAL_PROBABILITY_DECREASE_FACTOR_AFTER_MATCH, teammate, rival2)

    # Update the teammates relationship between the two rivals
    update_players_relationship_probability(teammates_prob_matrix, TEAMMATE_PROBABILITY_DECREASE_FACTOR_AFTER_MATCH, rival1, rival2)

    matchday.append(Match(Team(player, teammate), Team(rival1, rival2)))

  matches.append(matchday)


for index, matchday in enumerate(matches):
  print(f"Matchday {index}")

  for match in matchday:
    print(f"\t {match}")

print("")

for player in range(NUM_OF_PLAYERS):

    player_plays_matchdays = ""

    total_played = 0

    for index, matchday in enumerate(matches):
      player_plays_this_day = False

      for match in matchday:
          if match.includes_player(player):
              player_plays_this_day = True

      if player_plays_this_day:
        player_plays_matchdays += f" {index}"
        total_played += 1
      else:
        player_plays_matchdays += f"  "

    print(f"{PLAYER_NAMES[player]}: {player_plays_matchdays}: Total: {total_played}")

print("")

def write_player_pairs_table(player_pairs):
    player_pairs_header = "   "

    for player in range(NUM_OF_PLAYERS):
        player_pairs_header += f" {PLAYER_NAMES[player]}"

    print(player_pairs_header)

    for player in range(NUM_OF_PLAYERS):
        player_pairs_str = ""

        for i, pair in enumerate(player_pairs[player]):
            if i <= player:
                player_pairs_str += "  "
            else:
                player_pairs_str += f" {pair}"

        print(f"{PLAYER_NAMES[player]}: {player_pairs_str}")

player_pairs = [[]] * NUM_OF_PLAYERS

player_opponents = [[]] * NUM_OF_PLAYERS

for i in range(NUM_OF_PLAYERS):
    player_pairs[i] = [0] * NUM_OF_PLAYERS

    player_opponents[i] = [0] * NUM_OF_PLAYERS

for player in range(NUM_OF_PLAYERS):
    for matchday in matches:
        for match in matchday:
            pair_player = match.get_player_pair(player)

            if pair_player is not None:
                if pair_player < player:
                    player_pairs[pair_player][player] += 1

            opponents = match.get_player_opponents(player)

            if opponents is not None:
                for opponent in opponents:
                    if opponent < player:
                        player_opponents[opponent][player] += 1

print("PLAYING TOGETHER")

write_player_pairs_table(player_pairs)

print("")

print("PLAYING AS OPPONENTS")

write_player_pairs_table(player_opponents)
