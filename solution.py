
import cost_funcs.cf_same_spot as same_spot
import cost_funcs.cf_overlaps as overlaps
import cost_funcs.cf_category_balance as category_balance
import cost_funcs.cf_table_size as table_size

class Solution(object):
    def __init__(self, solution):
        self.solution = solution

        # FREQUENCIES
        # number refers to the group size
        self.overlaps2_freqs = overlaps.freqs(self.solution, 2)
        self.overlaps3_freqs = overlaps.freqs(self.solution, 3)
        self.same_spot_freqs = same_spot.freqs(self.solution)

        # COSTS
        self.cost_of_overlaps = overlaps.cost(self.overlaps2_freqs, 2) + \
                                overlaps.cost(self.overlaps3_freqs, 3)
        self.cost_of_same_spot = same_spot.cost(self.same_spot_freqs)
        self.cost_of_category_balance = category_balance.cost(solution)
        self.cost_of_table_size = table_size.cost(solution)
        self.cost = self.calc_cost()


    def calc_cost(self):
        cost = self.cost_of_same_spot + \
               self.cost_of_overlaps + \
               self.cost_of_category_balance + \
               self.cost_of_table_size
        return cost
