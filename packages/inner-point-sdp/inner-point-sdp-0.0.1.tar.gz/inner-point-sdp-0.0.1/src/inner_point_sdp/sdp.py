#!/usr/bin/env python
# coding: utf-8

# In[6]:


import numpy as np


# In[7]:


def get_next_step(A, S, X, b, C, y, mu):
    
    n = len(X)
    m = A.shape[0]
    
    # Definiere p, Q, R gemäß der Aufgabenstellung
    # Eigentlich sind das doch die Residuen?
    p = b - np.trace((A@X).T)
    Q = C - np.sum(y.reshape(A.shape[0], 1,1) * A, axis=0) - S
    R = mu * np.eye(n) - X @ S
    
    # Berechne das Inverse von S, wird später benötigt
    S_inv = np.linalg.solve(S, np.eye(n))
    
    # Berechne H von Hy_dach = rhs
    H = np.zeros((m,m))
    # vektorisierbar?
    for i in range(A.shape[0]):
        H[i] = np.ones(n)@(A[i] * (X @ A @ S_inv))@np.ones(n)
        
    #Berechne rhs
    rhs = p -  np.trace((A@(R @ S_inv - X @ Q@S_inv )).T)
    
    #Löse nach y_dach und ermittel dann S_dach und dann X_dach
    y_dach = np.linalg.solve(H, np.eye(m))@rhs
    S_dach = Q - np.sum(y_dach.reshape(A.shape[0], 1, 1) * A, axis=0)
    X_dach = (R - X @ S_dach) @ S_inv
    
    return X_dach, S_dach, y_dach


# In[3]:


def kurzschritt(C, A, b, epsilon=0.0000000001):
    
    n = len(C)
    
    # Parameter bestimmen: X, S, sigma  y?
    X_k, S_k, sigma = np.eye(n), np.eye(n), 1 / (20 * np.sqrt(n))
    y_k, mu_k = np.ones(A.shape[0]), np.trace(X_k @ S_k) / n
    
    while 1: 
        
        # Schritt 1
        mu_k = 1/n * np.trace(X_k.T @ S_k) * (1 - sigma)
        
        # Überprüfe ob mu_k die Abbruchbed. erfüllt
        if mu_k < epsilon:
            break

        #Schritt 2
        X_dach, S_dach, y_dach = get_next_step(A, S_k, X_k,b, C, y_k, mu_k)
        
        #Schritt 3
        X_k += 0.5 * (X_dach + X_dach.T)
        S_k += S_dach
        y_k += y_dach
        
    print(X_k)


# In[4]:


#Aufgabe 17
C = np.eye(3)
A = np.array([[0, 3, 0], [3, 0, 4], [0, 4, 0]]).reshape(1,3,3)
b = np.array([1])
kurzschritt(C, A, b)


# In[9]:


A_1 = np.array([[0, 3, 0], [3, 0, 4], [0, 4, 0]])
A_2 = np.array([[0, 0, 2], [0, 0, 0], [2, 0, 0]])
AA = np.array([A_1, A_2]).reshape(2,3,3)
y = np.array([2,3]).reshape(2,1,1)
bb = np.array([1,2])
kurzschritt(C, AA, bb)


# In[ ]:




