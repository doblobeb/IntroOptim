import numpy as np

np.set_printoptions(suppress=True, precision=5)
max_iter=100


def interior_point(C, A, b, epsi, alpha, init_x):
  x=init_x

  curr_iter=1
  acc=True

  while acc and curr_iter<max_iter:
    try:
      A_tilda = A @ np.diag(x)
      C_tilda = np.diag(x) @ C
      P = np.eye(A.shape[1]) - A_tilda.T @ np.linalg.inv(A_tilda @ A_tilda.T) @ A_tilda
      Cp = P @ C_tilda
      try:
        v = abs(min(Cp[Cp < 0]))
      except ValueError:
        print("The problem does not have solution!")
        err=True
        return None
      X_tilda = [[1]] * len(Cp) + Cp * (alpha / v)
      x_old=x
      x = (np.diag(x) @ X_tilda).reshape(1,-1).flatten()
      curr_iter += 1
      if np.linalg.norm(x-x_old)<10**(-epsi): acc=False
    except Exception:
      print("The method is not applicable!")
      err=True
      return None
  return x


C=np.array([[2],[1],[-8],[5],[0],[0]])
A=np.array([[-4,-5,-1,4,1,0],[5,1,2,1,0,1]])
epsi=3
init_x=np.array([1,1,1,1,20,7])
alpha=0.9
err=False
x1=interior_point(C,A,epsi,epsi,0.5,init_x)
x2=interior_point(C,A,epsi,epsi,0.9,init_x)
if not err:
  z1 = x1 @ C
  z2 = x2 @ C
  print(f"A vector of decision variables x* with alpha=0.5")
  print(x1)
  print(f"maximized value of the objective function z={z1}")
  print(f"A vector of decision variables x* with alpha=0.9")
  print(x2)
  print(f"maximized value of the objective function z={z2}")