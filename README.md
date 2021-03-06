# Predicting the price of used cars and recommending similar cars to the user

Machine learning web application that predicts the price of used cars based on car parameters. Furthermore, it incorporates a recommendation model for similar cars and it uses graphs to visualize price comparison between similar cars.


Data source -> Multiple online used cars markets


This project represents a full-stack Data Science project, from collecting raw data from a website to deploying the actual application to the streamlit framework. It incorporates ETL, EDA, ML, and model deployment as key features of this project. In addition, all of this could be orchestrated through the machine learning pipeline into a one single file. 

## ETL - Extract Transform Load

*Extract* - One of the first things that we need to accomplish is to extract raw data from a data source, in this case I webscraped a website.

*Transform* - Most of the work was around cleaning and transforming data into something more meaningful and easier for the model to consume and gain more insight in the end. 

*Load* - After successfully cleaning and transforming, data needs to be stored in some form of a database - in this case, a csv file, because the file contains <30k rows and it's the easiest way to work with data, for me (for now).

## EDA  - Explanatory Data Analysis

Data analysis was a part of cleaning and trasforming the data and you can gain more insight into what I did when it comes to ETL and EDA on this link -> [EDA, ETL](/Analysis2.0.ipynb) (*Note that the notebook has a formatting problem but if you download it you can run and check it out on the local machine*)


## ML - Machine Learning

The machine learning part was straightforward, I tried bunch of [ml algorithms](/ML_Pipe.ipynb)  and [neural network](/Neural Network.ipynb) and saved the best model.
Another thing, in addition to the machine learning model is a recommender system, the rule-based recommender system, to be precise. It is not perfect and it's based on intuition and domain knowledge to find similar cars.

## Model deployment 

I used the [streamlit](https://streamlit.io/) framework to deploy and share the application. Another alternative is to Dockerize the whole application and post it to DockerHub.

You can check out application here: https://share.streamlit.io/trsavi/machine-learning-web-app/main/mainApp.py

### How to use the application (since it's in Serbian)? 

  * On the left sidebar, there are parameters of the chosen vehicle which can be modified, and the main screen will change it's prediction price and graphs accordingly. At the bottom of the sidebar, there is a checkbox if you want to analyze and compare similar cars. When you click on it, there should be a list showing similar cars (if there are any) and you can choose any of them to be plotted on the graph with the chosen vehicle on the left sidebar.
   
  

