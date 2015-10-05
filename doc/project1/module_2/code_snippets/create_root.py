def create_root_node(self):
  root = VertexColoringState(self.start, self.gac, self.num_colors)
  self.gac.initialize(root.domains, root.state.constraints)
  self.gac.domain_filtering()
  return root