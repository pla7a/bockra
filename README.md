# Bockra
### Website for gauging sentiment of tweets/users/search-terms

For web-development, used Flask (deployed with nginx and gunicorn). For prediction model, I created a bag-of-words model using a large English-language dictionary. From this, I used a Bernoulli Naive Bayesian classifier on new entries (compared to old entries) taking into account likelihood and priors. I validated the model using k-fold cross validation (on the one training set) and found, consistently, an accuracy of 0.8-0.85. 

The main aim of project was primarily to become familiar with using Flask and deploying sites. There wasn't huge focus on the machine learning model (beyond a simple Naive Bayesian classifier and K-fold cross validation) or the front-end design. 

Libraries that are required are twitter-python, numpy, pandas, scikit-learn, and seaborn (if you enjoy pretty visualizations of the data). The training data used was the Sentiment140 dataset (which can be downloaded from http://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip). 

All API keys have been removed from the files. There are also redundant spotify methods in the main file due to a change in direction of the project.

A good next step might be to implement some mechanism to prevent dos through excessive use of twitter API (maybe a lightning payment of 300 satoshis (=$0.01) for each request).
