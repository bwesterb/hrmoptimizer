class EmptyInputException(Exception):
	pass

class BaseArgument(object):
	pass

class LabelArgument(BaseArgument):
	pass

class FloorArgument(BaseArgument):
	pass

class BaseInstruction(object):
	use_hand = False
	change_hand = False
	argumentType = None

	@classmethod
	def keyword(cls):
		return cls.__name__.upper()

	def __init__(self, argument):
		self.argument = argument

	def __str__(self):
		if self.argumentType:
			return "%s %s" % (self.keyword(), self.argument)
		return self.keyword()

class Inbox(BaseInstruction):
	change_hand = True

	def do(self, state):
		if len(state.input) == 0:
			raise EmptyInputException()
		state.hand = state.input.pop(0)

class Outbox(BaseInstruction):
	use_hand = True
	change_hand = True

	def do(self, state):
		state.assertHandNotEmpty()
		state.output.append(state.hand)

class CopyFrom(BaseInstruction):
	change_hand = True
	argumentType = FloorArgument

	def do(self, state):
		state.hand = state.get(self.argument)

class CopyTo(BaseInstruction):
	use_hand = True
	argumentType = FloorArgument

	def do(self, state):
		state.assertHandNotEmpty()
		state.set(self.argument, state.hand)

class Add(BaseInstruction):
	use_hand = True
	change_hand = True
	argumentType = FloorArgument

	def do(self, state):
		state.assertHandNotEmpty()
		state.hand += state.get(self.argument)

class Sub(BaseInstruction):
	use_hand = True
	change_hand = True
	argumentType = FloorArgument

	def do(self, state):
		state.assertHandNotEmpty()
		state.hand -= state.get(self.argument)

class BumpPlus(BaseInstruction):
	change_hand = True
	argumentType = FloorArgument

	def do(self, state):
		state.hand = state.get(self.argument)+1
		state.set(self.argument, state.hand)

class BumpMin(BaseInstruction):
	change_hand = True
	argumentType = FloorArgument

	def do(self, state):
		state.hand = state.get(self.argument)-1
		state.set(self.argument, state.hand)

class BaseJumpInstruction(BaseInstruction):
	pass

class Jump(BaseJumpInstruction):
	argumentType = LabelArgument

class JumpZ(BaseJumpInstruction):
	use_hand = True
	argumentType = LabelArgument

class JumpNeg(BaseJumpInstruction):
	use_hand = True
	argumentType = LabelArgument

all = [Inbox, Outbox, CopyFrom, CopyTo, Add, Sub, BumpPlus, BumpMin, Jump, JumpZ, JumpNeg]