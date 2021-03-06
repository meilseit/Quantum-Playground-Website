# Quantum-Playground-Website

**Project Summery:** 
The introduction of quantum mechanics at the undergraduate level poses one of the greatest leaps for students in physics education. Despite this, there is sparse practice and exposure to anything but the proverbial analytical solutions to the schrödinger equation. This project proposes a more flexible and available web-hosted approach to computational solutions of the schrödinger equations. This quantum sandbox provides user-determined well-size,  potential functions, and particle type. By implementing a LAPACK algorithm for solving eigenvalue problems in conjunction with approximating the hamiltonian using a finite difference method, the program delivers the energy eigenvalues and converging wavefunctions to custom potentials. With energy eigenvalues accurate to the third decimal point, this algorithm is an accurate and efficient approach to solving and visualizing bound state wavefunction behavior.
### Thesis Paper
This Full stack website was also the topic of my thesis research paper. For those serioulsy interested in the details of development I have linked my paper below. [Thesis Paper](https://github.com/meilseit/Quantum-Playground-Website/blob/master/ThesisPaper.pdf)
## The Website
The website itself is built in python using a Django web frame work. The structure is broken up into pieces which are tagged below:
- [Nuts and Bolts](https://github.com/meilseit/Quantum-Playground-Website/tree/master/website/nuts_bolts): This folder defines all the classes and machinery needed to construct the solutions to the Schrödinger equation. Hub.py is module that holds the wavefunction, energy and potential objects.
- [View](https://github.com/meilseit/Quantum-Playground-Website/blob/master/website/views.py):  This .py file is the work horse of the website and is in charge of manganging POST and GET requests from the frontend. In addition views handles python injection into the HTML template.
- [Models](https://github.com/meilseit/Quantum-Playground-Website/blob/master/website/models.py): This .py file holds all the relevent models that create tables in the database.
- [Functions](https://github.com/meilseit/Quantum-Playground-Website/blob/master/website/functions.py): This module holds many helper functions used in the view.py to process data and generate expectation values to be diplayed on the website.
- [Tasks](https://github.com/meilseit/Quantum-Playground-Website/blob/master/website/tasks.py): This .py file defines the async task that should be placed in the redis queue to help ease the HTTP traffic. This allows us to display results as they become avaliable instead of waiting minutes for all numerical solutions.
- [Static](https://github.com/meilseit/Quantum-Playground-Website/tree/master/website/static/website): This folder not only holds the style.css but all the the javascript functions required for rendering the graphs. Also preset data is stored here as .npz files.

### Underlying Algorithm:
The underlying algorithm we are using is LAPACK eigenvalue and eigen vector routine from the scipy python library. The setup is contianed in a class called [Sandbox](https://github.com/meilseit/Quantum-Playground-Website/blob/master/website/nuts_bolts/hub.py). 
### Technologies Used:
- **Django** as web frame work to hold the python algorithm and website
- **Heroku** was used to deploy the website
- **SqlLite** was used as the local database
- **Postgresql** was used as the remote database 
- **Redis** facilited a cache and queue system to preform async calculations
- **ApexCharts** a javascript graphing library
- **Bootstrap** was used for styling the website
- **Numpy** library provided support for matrix minipulation
- **Scipy** for accsess to the LAPACK algorithms

## The Physics

### Solving the Schrödinger equation:
Solutions to this problem are typically conducted in two frameworks: 
- Differential Equations:
A common approach that was abandoned during this project is the shooting method. This approach is fast but very sensitive due to [numerical instablity](https://geo.libretexts.org/Bookshelves/Meteorology_and_Climate_Science/Book%3A_Practical_Meteorology_(Stull)/20%3A_Numerical_Weather_Prediction_(NWP)/20.03%3A_Section_4-#:~:text=3.-,Numerical%20Instability,one%20cause%20of%20numerical%20instability.)

<img height= "55" width="200" alt="Screen Shot 2022-05-05 at 11 09 25 AM" src="https://user-images.githubusercontent.com/75337068/166976455-00d90236-92b7-495f-8349-69f02dd101cb.png">

- Eingenvalue Equations:
Although this form of solution is slower and for memory intesive due to large matrix calculations, it promises orthogonal wavefunctions that are far less sensitive.
<img height= "55" width="160" alt="Screen Shot 2022-05-05 at 11 09 34 AM" src="https://user-images.githubusercontent.com/75337068/166976440-d302c4c3-8003-42b1-8526-eeba3e0dc6fa.png">
This equation is composed of hermtian matrix and corresponding eigenvalues.


### Error and Accuracy:
- **How Accurate Are Our Results?**
The below graph depicts the accuracy of the algorithm when it comes to eigenvalues i.e. bound states. The orange dots represent the analytic solutions to a 1D finite well. The blue dots are the values generated by the algorithm. The size of the blue dots are representative of the error at that index. Note: the error is blown up by a factor of 10^7 to be visible.
![finitequantumwell](https://user-images.githubusercontent.com/75337068/166973123-c96e16ad-eb44-4f6b-870e-eb08f751a5a5.png)
The largest precent error for all 220 states was only ±0.006877%. This is very good but conducted at resolutions not capable of a website (n=10,000) Realistically we would expect ±2.0000% in eigenvalue accuracy with a much smaller sample rate (n=1000).

- **How Do We Esitmate Error?**
Before we can begin estimating the error of the results we need to estimate differentials to construct the hermitian matrix
mentioned above. To do this it is common to use the finite difference method. The error associated with the corresponding matrix is dependent on the resolution.
<img width="316" alt="Screen Shot 2022-05-05 at 11 41 12 AM" src="https://user-images.githubusercontent.com/75337068/166981560-0e8c82fb-7a05-4d3a-849b-df7e0d6c248a.png">


Now that we have a hermtian tridiagonal matrix we can use the LAPACK routine to extract eigenvalues. The algorithms corresponding error is depicted below. 

<img width="349" alt="Screen Shot 2022-05-05 at 11 41 07 AM" src="https://user-images.githubusercontent.com/75337068/166981576-68d79346-cec3-47e6-917f-e1c8ea97d655.png">

Epsilon corresponds to machine precision. P(n) corresponds to a moderatly increase function of n. For example P(n) = 10

Maybe the most important thing to understand when trying to maximize the preformance of this algorithm is to notice that as n>> we see better results for estimating the hermitian matrix. However at the same time we produce worse results for the eigenvalues. This relationship is depicted below and suggests that there is a sweet spot to extracting the most accurate results.

<img width="797" alt="Screen Shot 2022-05-05 at 12 01 16 PM" src="https://user-images.githubusercontent.com/75337068/166984883-c7fb7a74-8f58-4e62-bcae-b5dd07a5625c.png">

## Final Considerations:
- **Degenerate States**
When there is a certain degree of symmetry in the potential well the algorithm will return degenrate energy states. As of now there is no good way to collect the degnerate states and graph there superposition. Because of this user should be aware that sometimes reults may not be complete.








