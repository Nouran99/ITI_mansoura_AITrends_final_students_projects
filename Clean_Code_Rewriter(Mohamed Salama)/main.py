# main.py
from crew_make import run_code_improvement_workflow

def main():
    # Example code to analyze and improve
    code_snippet = """
def x(a,b):
  c = 0
  for i in a:
    if i>10:
      c+=i
    else:
      for j in b:
        if j<5:
          c+=j*2
        else:
          c-=1
  print("Done")
  return c
a = [4, 15, 3, 22]
b = [1, 5, 3]
print(x(a,b))


"""
    
    # Run the code improvement workflow
    result = run_code_improvement_workflow(code_snippet)
    
    # Write result to file to avoid recursion issues
    with open('result.txt', 'w') as f:
        f.write(str(result))
    print("Result saved to result.txt")

if __name__ == "__main__":  # Fix syntax here
    main()