def generate_all_successors():
  successors = []

  viable_domains = get_domains_not_empty()
  sorted_domains = sort_by_domain_length_asc()
  (variable, domain) = sorted_domains.pop(0)

  for color in domain:
    new_domains = new_domain_dict_instance_with_old_references(domains)
    new_domains[variable] = [color]

    successor = VertexColoringState(new_domains)
    result = GAC.rerun(new_domains, variable)

    if successor.is_solution():
      return [successor]

    if result:
      successors.append(successor)

  return successors