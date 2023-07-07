A dynamic map is updated every 4 hours, which presents the risk level of fire incident in Greece.

### https://mbolotis.github.io/greekfireprediction.github.io/


# Fire Prediction for Greece

The scope of this project is to create a real-time prediction model for wildfires in Greece and export this model through a web application.

## Description

The Application wil use a model which will use appropriate data to predict real-time probability of wildfires in each district of Greece. 
Almost 53.983 conflagrations occurred in Greece between 1980 and 2016 and for Greece this is a major and chronic issue. We are all interested in our forests especially during the last years that climate change causes several problems to our lives. 

## Getting Started

### Goal

The aim is to exploit existing free to use data, in order to train machine learning models to predict the risk of fire incidents.

Our hypothesis is that by collectinng historical weather data as well as fire incidents, we can combine and use them to create machine learning models.

The model can be used in real-time to provide a risk level of fire incident

### Tools

- NumPy and Pandas: For data processing
- Sklearn, Tensoflow, Keras: To implements the various machine learning algorithms
- Folium: To visualize the results on a dynamic map
- BeautifulSoup and Requests: For the web-scraping process
- GitHub Pages host the web application 
- GitHub Actions perform the Continuous integration (CI) by updating the map every 4 hours 

### General Details 

1. Collect past data for fire incidents in Greece as well as temperature, wind speed and dew point
2. Create a Machine Learning model based on the collected data
3. Scrape the current teperature, wind speed and dew point of each area to feed my model and classify the area according to its risk level
4. Fetch the information on a dynamic map

## License

This project is licensed under the Apache-2.0 License - see the LICENSE.md file for details
