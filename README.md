![Sprint 1](https://www.institucionalcolombia.com/wp-content/uploads/2020/10/conershop_lista_de_mercado_en_un_app.jpg)

# Cornershop´s Data Science Test

## Abstract

In this case study, I developed a solution to predict how long a delivery order takes to be completed. The project was divided into several small steps, *e.g.* Data Handling and Understanding, Statistical Analysis, Exploratory Data Analysis, Preprocess and Modeling. I implemented four different models: Linear Regression as a Baseline Model, Support Vector Regressor and Boosting Models, and compared their results regarding the prdictions for the total time of completed deliveries. Moreover, I studied some possible combinations of engineering new features and fine-tuned the Champion Model using two different sets of resources.

The corresponding results are located at the folder [mvp](https://github.com/broilo/cornershop/tree/main/mvp) where:
1. **__preprocess.py** is a py-script with a class of functions associated with the data preprocess step
2. **mvp.py** is a another python-script which loads the dataset under prediction and performs the necessary data preprocessing. Moreover, this script also load the trainned model and predict the corresponding label/target values.
3. **20220403_outputs.csv** represents the predicted results. First column contains the order identification and the second (y_hat) is the corresponding order's prediction.

and the folder [notebooks](https://github.com/broilo/cornershop/tree/main/notebooks) contains ipynb's associated with those several small steps previously mentioned and properly documented. This folder also contains two outliers dictionary and the corresponding trained model **20220403_set4_XGBRegressor.sav** (XGBoost spolied!).

## First Things First: A brief introduction.

Online shopping represents a huge part of the sales market. And currently this model of business is bigger than it has ever been and most probably will keep growing more and more. During this last couple of years, the COVID-19 pandemic forced us to stay at home with little oportunities, or none, to go out and shopping. While retail market simply vanished at plain sight, the E-Commerce has grown. Food, medications, clothes... All sort of products, even supermarket deliveries! We're more connected than ever.

Cornershop has operations in several cities and countries, delivering thousands of orders every day. In order to deliver these orders on time Cornershop depends on good estimations of how much time the shopper needs to complete the order. The process of achieving this estimations presents many challenges. For example, missed product identification in an order or the lack of how much itens of this product the order contains.

## File description and data fields
***order_products.csv:***
- order_id: ID of the order
- product_id: ID of the product
- quantity: The quantity ordered of this product
- buy_unit: The unit of the product (KG/UN)

***orders.csv:***
- order_id: ID of the order
- lat: The latitude of the delivery location
- lng: The longitude of the delivery location
- promised_time: The delivery time promised to the user
- on_demand: If true, the order was promised to be delivered in less than X minutes
- shopper_id: ID representing the shopper completed the order.
- store_branch_id: ID of the store branch
- total_minutes: The total minutes it took to complete the order (label)

***shopper.csv***
- shopper_id: ID of the shopper
- seniority: The experience level of the shopper.
- found_rate: Percentage of products found by shopper historical.
- picking_speed: Historical picking speed, products pr minutes.
- accepted_rate: Percentage of orders historically accepted by shopper
- rating: client rating of shopper

***storebranch.csv:***
- store_branch_id: ID of the store branch
- store: ID representing the store
- lat: Latitude of the branch location
- lng: Longitude of the branch location

## [Data Merging](https://github.com/broilo/cornershop/blob/main/notebooks/part1_data_merging.ipynb)

The first part of the case study is associated with the data handlings and undertandig. For example, there're four different datasets all related within one another by means os some specific information. These data merging were performed as follws:

### Merge 1 $\to$ orders & shoppers

* **order_id**: primary key
* **shopper_id**: foreign key

        mg1 =  orders.merge(
            shopper,
            how='left',
            left_on=['shopper_id'],
            right_on=['shopper_id'])

### Merge 2 $\to$ mg1 & storebranch

* **order_id**: primary key
* **store_branch_id**: foreign key

        mg2 = mg1.merge(
            storebranch,
            how='left',
            left_on=['store_branch_id'],
            right_on=['store_branch_id'])

### Merge 3 $\to$ mg2 & order_products

* **order_id**: primary key
* **order_id**: foreign key

        mg3 = mg2.merge(
            order_products,
            how='left',
            left_on=['order_id'],
            right_on=['order_id'])

At the end, the process resulted into a single dataset with a cardinality of 198522 tuple/rows and a degree of 19 attributes/columns. 

**Notice that** there're orders identifications in the orders dataset that aren't in order_products dataset. Therefore, to take into account all order identifications, *i.e* all deliver orders, the correct join must be a left one.

### Dataset to train and test

This dataset were properly constructed by means of considering all orders associated with non-missing total minutes values (which is the label to be predited). Therefore, this dataset has a shape of 158325 rows and 19 columns.

### Dataset to predict: Simmulating the real world

Following the same logic as above, only with the difference that this dataset is associated with the missing values of the total minutes label columns. At the end, the corersponding shape is 40197 rows.

## [Statistical Analysis](http://localhost:8888/notebooks/Documents/Arbeit/Personal/projects/cornershop/notebooks/part2_analytical_record.ipynb)

The second part of this case project is associated with to consolidade the analytical record regarding the uderlying data information.

### Orders & Products information

The quantity resource corresponds to how much of a single product the order posses. *E.g* the maximum value found is of 70 and minimum is of 0.055. However, the values in it might be in the dimensions of "units of bits of products" (1,2,3,...) or a produtc's wight (1.7, 2.3, 3,...).

TO BE CONTINUED...


