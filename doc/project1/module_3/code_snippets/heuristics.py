def heuristic_evaluation():
  return sum([math.log(len(domain)) for domain in domains.values()])