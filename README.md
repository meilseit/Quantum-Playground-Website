# Quantum-Playground-Website
**Project Summery:** 
The introduction of quantum mechanics at the undergraduate level poses one of the greatest leaps for students in physics education. Despite this, there is sparse practice and exposure to anything but the proverbial analytical solutions to the schrödinger equation. This paper proposes a more flexible and available web-hosted approach to computational solutions of the schrödinger equations. This quantum sandbox provides user-determined well-size,  potential functions, and particle type. By implementing a LAPACK algorithm for solving eigenvalue problems in conjunction with approximating the hamiltonian using a finite difference method, the program delivers the energy eigenvalues and converging wavefunctions to custom potentials. With energy eigenvalues accurate to the third decimal point, this algorithm is an accurate and efficient approach to solving and visualizing bound state wavefunction behavior.
## The Website
The website itself is built in python using a Django web frame work. The structure is broken up into pieces which are tagged below:
### Underlying Algorithm:
The underlying algorithm we are using is LAPACK eigenvalue and eigen vector routine from the scipy python library. The setup is contianed in a class called [Sandbox](). The 
### Technologies Used:
- **Django** as web frame work to hold the python algorithm and website
- **Heroku** was used to deploy the website
- **SqlLite** was used as the local database
- **Postgresql** was used as the remote database 
- **Redis** facilited a chache and queue system to preform async calculations
- **ApexCharts** a javascript graphing library
- **Bootstrap** was used for styling the website
- **Numpy** library provided support for matrix minipulation
- **Scipy** for accsess to the LAPACK algorithms

## The Physics

### Solving the Schrödinger equation:


### Error and Accuracy:
- **How Accurate Are Our Results?**


ffdfdddddd
- **How Do We Esitmate Error?**












