class ExecutionStrategies(object):
    """
    Enum like object listing the types of execution strategies.
    """
    PRE_COMPUTE = 0
    PARALLEL = 1


class ExecutionEngine(object):
    """
    Class to perform serial execution of a Sequence evaluation.
    """
    def evaluate(self, sequence, transformations):
        """
        Execute the sequence of transformations in serial
        :param sequence: Sequence to evaluation
        :param transformations: Transformations to apply
        :return: Resulting sequence or value
        """
        # pylint: disable=no-self-use
        result = sequence
        for transform in transformations:
            strategies = transform.execution_strategies
            if strategies is not None and ExecutionStrategies.PRE_COMPUTE in strategies:
                result = transform.function(list(result))
            else:
                result = transform.function(result)
        return iter(result)
