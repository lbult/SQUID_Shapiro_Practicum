import numpy as np

data = [[4.287667317427189e-06, 4.365466989007236e-06, 2111.1111111111113],
        [3.311896038487763e-06, 3.2166598866369103e-06, 1555.5555555555557],
        #[4.05427764624777e-06, 4.900811098711807e-06, 2370.0],
        #[3.110094708501369e-06, 2.502101868962568e-06, 1210.0],
        [2.8138013337849888e-06, 2.9983865371865486e-06, 1450.0],
        [3.2668074659962633e-06, 3.246528871298539e-06, 1570.0],
        #[2.694686583560705e-06, 3.0397435928718803e-06, 1470.0],
        [3.11663456050873e-06, 3.3912785661972e-06, 1640.0],
        [3.3777108929421115e-06, 3.4326356218825316e-06, 1660.0],
        [3.411996848849081e-06, 3.494671205410529e-06, 1690.0],
        [3.5520232916290446e-06, 3.5567067889385267e-06, 1720.0]]

# use a 2-sigma criterion for outlier elimination

eh = []
deltas = []
hes = []
for i in data:
    he = (i[2]*10**6)/(i[0]*2)
    hes.append(he)
    delta = abs(he-2.4179671*10**14)
    deltas.append(delta)
    eh.append(he/(2.4179671*10**14))

print("Mean e/h: " + str(np.mean(hes)))
print("Std e/h: " + str(np.std(hes)))
print("Uncertainty e/h: " + str(np.std(hes)/(len(hes))**0.5))

print("Mean e/h (%) (of e/h real)): " + str(np.mean(hes)/(2.4179671*10**14)))
print("Std e/h (%) (of e/h real): " + str(np.std(hes)/(2.4179671*10**14)))
print("Uncertainty e/h (%) (of e/h real): " + str(np.std(hes)/(2.4179671*10**14)/(len(hes))**0.5))

print(eh)
#print("Mean delta: " + str(np.mean(deltas)))
#print("Std delta: " + str(np.std(deltas)))
#print("Uncertainty delta: " + str(np.std(deltas)/(len(deltas))**0.5))
