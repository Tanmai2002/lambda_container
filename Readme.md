Steps:
1. Create a global variable FUNCTION_DIR pointing to a directory(Yaha sare store honge) where we want to store all data(Generally mac mein export FUNCTION_DIR=xyz)
2. Now write all code in app.py
3. create a ecr repository on aws(make sure its private)
4. there you will find commands in view command option execute all steps(High chances of getting push denied. )
5. After it is successfully created, go to lambda, select container image option , put your function name, select image yoou created earlier.