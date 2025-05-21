from io import BytesIO
import base64
import matplotlib.pyplot as plt

# Defines function to create graph
def get_graph():
    # Creates a BytesIO buffer for the image
    buffer = BytesIO()

    # Creates plot with a BytesIO object as a file-like object
    plt.savefig(buffer, format="png")

    # Sets cursor to beginning of the stream
    buffer.seek(0)

    # Retrieves content of the file
    image_png = buffer.getvalue()

    # Encodes the bytes-like object
    graph = base64.b64encode(image_png)

    # Decodes to get the string as output
    graph = graph.decode("utf-8")

    # Frees up the memory of buffer
    buffer.close()

    # Returns the image/graph
    return graph

# Defines function to implement logic to prepare the chart based on user input
def get_chart(chart_type, data, **kwargs):
    # Switches plot backend to Anti-Grain Geometry to write to file
    plt.switch_backend("AGG")

    # Specifies figure size
    fig = plt.figure(figsize=(6,3))

    # Determines layout of each chart_type
    if chart_type == "#1":
        # Plots bar chart between recipe name on x-axis and cooking_time on y-axis
        plt.bar(data["name"], data["cooking_time"])
        plt.xlabel("Recipe Names")
        plt.ylabel("Cooking Time (In Minutes)")
        plt.xticks(rotation=45, ha="right")

    elif chart_type == "#2":
        # Generates pie chart based on difficulty with difficulties as labels
        labels = data["difficulty"].value_counts().index
        sizes = data["difficulty"].value_counts().values
        plt.pie(sizes, labels=labels, autopct="%1.1f%%")

    elif chart_type == "#3":
        # Plots line chart between recipe name on x-axis and number of ingredients on y-axis
        plt.plot(data["name"], data["number_of_ingredients"], marker="o")
        plt.xlabel("Recipes Names")
        plt.ylabel("Number of Ingredients")
        plt.xticks(rotation=45, ha="right")

    else:
        print("Unknown chart type")

    # Specifies layout details
    plt.tight_layout()

    # Returns the graph to file
    chart = get_graph()
    return chart