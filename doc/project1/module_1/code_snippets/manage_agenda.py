def open_push(self, opened, node):
  """ Push node onto opened according to mode, and set status """
  node.status = C.status.OPEN

  if self.mode is C.search_mode.A_STAR:
    q.heappush(opened, (node.f, node))
  elif self.mode is C.search_mode.DFS or self.mode is C.search_mode.BFS:
    opened.append(node)

def open_pop(self, opened):
  """Pop node from opened according to mode """
  if self.mode is C.search_mode.A_STAR:
    return q.heappop(opened)[1]
  elif self.mode is C.search_mode.DFS:
    return opened.pop()
  elif self.mode is C.search_mode.BFS:
    return opened.pop(0)
