def readNumber(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    keta = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * keta
      keta /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  priority = 0
  return token, index, priority


def readPlus(line, index):
  token = {'type': 'PLUS'}
  priority = 2
  return token, index + 1, priority


def readMinus(line, index):
  token = {'type': 'MINUS'}
  priority = 2
  return token, index + 1, priority


def readMultipled(line, index):
  token = {'type': 'MULTI'}
  priority = 1
  return token, index + 1, priority


def readDevided(line, index):
  token = {'type': 'DEVIDED'}
  priority = 1
  return token, index + 1, priority


def tokenize(line):
  tokens = []
  priorities = []
  index = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index, priority) = readNumber(line, index)
    elif line[index] == '+':
      (token, index, priority) = readPlus(line, index)
    elif line[index] == '-':
      (token, index, priority) = readMinus(line, index)
    elif line[index] == '*':
      (token, index, priority) = readMultipled(line, index)
    elif line[index] == '/':
      (token, index, priority) = readDevided(line, index)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
    priorities.append(priority)
  priorities.insert(len(line), "0") # Insert a dummy '0' priority
  return tokens, priorities

def processing(index, tokens, priorities):
    while priorities[index + 1] == 1:
        if(tokens[index + 2]['type'] == 'NUMBER'):
            if tokens[index + 1]['type'] == 'MULTI':
                tokens[index + 2]['number'] *= tokens[index]['number']
            else:
                tokens[index + 2]['number'] = tokens[index]['number'] / tokens[index + 2]['number']
        else:
            print('ERROR')
            exit(1)
        index += 2
    return index, tokens
    
def evaluate(tokens, priorities):
  answer = 0
  tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  priorities.insert(0, "2") # Insert a dummy '2' priority
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
        if tokens[index - 1]['type'] == 'PLUS':
            if priorities[index + 1] == 1:
                (index,tokens) = processing(index, tokens, priorities)
            answer += tokens[index]['number']
        elif tokens[index - 1]['type'] == 'MINUS':
            if priorities[index + 1] == 1:
                (index,tokens) = processing(index, tokens, priorities)
            answer -= tokens[index]['number']
        else:
            print('Invalid syntax')
            exit(1)
    index += 1
  return answer  
   
def test(line):
  (tokens, priorities) = tokenize(line)
  actualAnswer = evaluate(tokens, priorities)
  expectedAnswer = eval(line)
  if abs(actualAnswer - expectedAnswer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expectedAnswer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
  print("==== Test started! ====")
  test("1+2")
  test("1.0+2.1-3")
  test("3*4+4*6-9/3") #整数のみの加減乗除
  test("2.5*4+12.25*8.0-120/2.5") #小数を含む加減乗除
  test("-1.25*8*5/30-3.3*2.2/8*5+2.8/3*1.35") #無限小数を含む加減乗除
  test("3**4")#不適切な入力1
  test("4/6^2")#不適切な入力2
  print("==== Test finished! ====\n")

runTest()

while True:
  print('> ', end="")
  line = input()
  (tokens, priorities) = tokenize(line)
  answer = evaluate(tokens, priorities)
  print("answer = %f\n" % answer)
