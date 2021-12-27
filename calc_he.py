import numpy as np

data = [[4.287667317427189e-06, 4.365466989007236e-06, 2111.1111111111113],
        [3.311896038487763e-06, 3.2166598866369103e-06, 1555.5555555555557],
        [4.05427764624777e-06, 4.900811098711807e-06, 2370.0],
        [3.110094708501369e-06, 2.502101868962568e-06, 1210.0],
        [2.8138013337849888e-06, 2.9983865371865486e-06, 1450.0],
        [3.2668074659962633e-06, 3.246528871298539e-06, 1570.0],
        [2.694686583560705e-06, 3.0397435928718803e-06, 1470.0],
        [3.11663456050873e-06, 3.3912785661972e-06, 1640.0]]

deltas = []
hes = []
for i in data:
    he = (i[2]*10**6)/(i[0]*2)
    hes.append(he)
    delta = abs(he-2.4179671*10**14)
    deltas.append(delta)

print("Mean e/h: " + str(np.mean(hes)))
print("Std e/h: " + str(np.std(hes)))
print("Uncertainty e/h: " + str(np.std(hes)/(len(hes))**0.5))

print("Mean e/h (%) (of e/h real)): " + str(np.mean(hes)/(2.4179671*10**14)))
print("Std e/h (%) (of e/h real): " + str(np.std(hes)/(2.4179671*10**14)))
print("Uncertainty e/h (%) (of e/h real): " + str(np.std(hes)/(2.4179671*10**14)/(len(hes))**0.5))

print("Mean delta: " + str(np.mean(deltas)))
print("Std delta: " + str(np.std(deltas)))
print("Uncertainty delta: " + str(np.std(deltas)/(len(deltas))**0.5))
