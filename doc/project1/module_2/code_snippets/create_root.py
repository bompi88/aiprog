def create_root_node():
  root = VertexColoringState(start)
  gac.initialize(root.domains, root.constraints)
  gac.domain_filtering()
  return root