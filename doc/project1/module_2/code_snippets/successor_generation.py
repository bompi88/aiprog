def generate_all_successors(self):
  successors = []

  viable_domains = {
    k: domain for k, domain in self.domains.items() if len(domain) > 1
  }

  sorted_domains = OrderedDict(
    sorted(viable_domains.items(), key=lambda x: -len(x[1]))
  )

  (key, domain) = sorted_domains.popitem()

  for color in domain:
    new_domains = domaincopy(self.domains)
    new_domains[key] = [color]

    successor = VertexColoringState(
      self.state, self.gac, self.num_colors, new_domains,
      self._solution_length + 1
    )
    result = self.gac.rerun(new_domains, key)

    if successor.is_solution():
      return [successor]

    if result:
      successors.append(successor)

  return successors