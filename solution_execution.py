from validate_puzzle import Puzzle

solution = [[2,3,1], [3,1,2], [1,2,3]]
constraints = [((1,2),(1,1)), ((1,2), (1,3)), ((2,1), (2,2)), ((2,3), (2,2)), ((3,2), (3,1)), ((3,3), (3,2))]
N = 5
p = Puzzle(N, constraints, solution)

#print(solution[0][2])
result = p.validate()

if result:
    print("Your solution is accepted - {}".format(result))
else:
    print("your solution is not accepted - {}".format(result))
