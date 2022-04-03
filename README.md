![Sprint 1](https://www.institucionalcolombia.com/wp-content/uploads/2020/10/conershop_lista_de_mercado_en_un_app.jpg)

# Cornershop´s Data Science Test

## Abstract

In this case study, I developed a solution to predict how long a delivery order takes to be completed. The project was divided into several small steps, *e.g.* Data Handling and Understanding, Statistical Analysis, Exploratory Data Analysis, Preprocess and Modeling. I implemented four different models: Linear Regression as a Baseline Model, Support Vector Regressor and Boosting Models, and compared their results regarding the prdictions for the total time of completed deliveries. Moreover, I studied some possible combinations of engineering new features and fine-tuned the Champion Model using two different sets of resources.

The corresponding results are located at the folder:
  
    ./mvp/
    
where:
1. **__preprocess.py** is a py-script with a class of functions associated with the data preprocess step
2. **mvp.py** is a another python-script which loads the dataset under prediction and performs the necessary data preprocessing. Moreover, this script also load the trainned model and predict the corresponding label/target values.
3. **20220403_outputs.csv** represents the predicted results. First column contains the order identification and the second (y_hat) is the corresponding order's prediction.
4. **./notebooks/** folder contains ipynb's associated with those several small steps previously mentioned and properly documented.

## First Things First: A brief introduction.

Cornershop has operations in several cities and countries, delivering thousands of orders every day. In order to deliver these orders on time Cornershop depends on good estimations of how much time the shopper needs to complete the order.





