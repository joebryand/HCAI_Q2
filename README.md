Path recognition HCAI_Q2 

Ik heb onderzoek gedaan naar het trainen van een model om beweegpatronen van bijen te onderscheiden. In deze repository staat de code van dit project. De code bestaat uit drie onderdelen:
- path_generator.py hierin worden paden van bijen gegenereerd. Hiervoor zijn verschillende klassen gebruikt, die later weer onderscheidde kunnen worden. Deze code genereerd twee csv's, een met de paden en een met de labels.
- clustering_kmeans.py en clustering_LSTM.py hierin worden de paden in twee groepen geclusterd. bij de ene met kmeans en de andere met LSTM. Beide codes nemen de twee csv's als input, en de verwerking van de data is zo simple mogelijk gehouden om de modellen goed te kunnen vergelijken.
- visualisation_tool met deze code kunnen de gegenereerde paden worden weergegeven. hiervoor kan gekozen worden het pad te tekeken en/of de bij zelf. tip! gebruik een laag aantal bijen om het goed te kunnen bekijken. 
