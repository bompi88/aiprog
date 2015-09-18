class HelloWorldPrintable(object):
  def __init__(self):
    self.string = 'hello, world!'

  def __str__(self):
    return self.string

print(HelloWorldPrintable())
