import pandas as pd
from ipyvizzu import Config, Data, Style
from ipyvizzustory import Slide, Step, Story

# Create data object, read csv to data frame and add data frame to data object.
example_data = Data()
example_df = pd.read_csv(
    #"complex.csv",
    "https://raw.githubusercontent.com/vizzuhq/ipyvizzu-story/main/docs/examples/demo/ipyvizzu-story_example.csv",
    dtype={"Year": str},
)
example_data.add_data_frame(example_df)
# Set the style of the charts in the story
example_style = Style(
    {
        "plot": {
            "yAxis": {
                "label": {
                    "fontSize": "1em",
                    "paddingRight": "1.2em",
                },
                "title": {"color": "#ffffff00"},
            },
            "xAxis": {
                "label": {
                    "angle": "2.5",
                    "fontSize": "1.1em",
                    "paddingRight": "0em",
                    "paddingTop": "1em",
                },
                "title": {"fontSize": "0.8em", "paddingTop": "2.5em"},
            },
        },
        "logo": {"width": "5em"},
    }
)

# Create story object, add data and style settings to it
# and set the size of the HTML element
# that appears within the notebook.
story = Story(data=example_data, style=example_style)
story.set_size(1000, 1000)

# Add the first slide,
# containing a single animation step that sets the initial chart.
slide1 = Slide(
    Step(
        # Only include rows where the Function value != Defense
        Data.filter("record.Function !== 'Defense'"),
        Config(
            {
                "channels": {
                    "y": {
                        "set": ["Amount[B$]", "Function"],
                        # Set the range of the y-axis
                        # to the min and max of the data being shown
                        # default value is 110% of the maximum value.
                        "range": {"min": "0%", "max": "100%"},
                    },
                    "x": {"set": ["Year"]},
                    "color": "Function",
                },
                "title": "Stacked Area Chart - U.S. R&D Budget in 1955-2020",
                "geometry": "area",
            }
        ),
    )
)
# Add the slide to the story
story.add_slide(slide1)

# Show components side-by-side
slide2 = Slide(
    Step(
        Config(
            {
                "split": True,
                "title": "Show Components Side by Side",
            }
        )
    )
)
story.add_slide(slide2)

# This slide contains multiple steps.
# Note that the slide is created as an empty object,
# then steps are added to it one-by-one.
slide3 = Slide()

# Step 1 - let's get back to the previous view
slide3.add_step(Step(Config({"split": False})))
# Step 2 - Add the defense function to the chart by removing it from the filter
slide3.add_step(
    Step(
        Data.filter(None),
        Config({"title": "Add New Category While Keeping the Context"}),
    )
)
# Add the multi-step slide to the story, just like any other slide.
story.add_slide(slide3)

# Show share of components
slide4 = Slide(
    Step(
        Config({"align": "stretch", "title": "Show Share of Components (%)"})
    )
)
story.add_slide(slide4)

# Compare data from 1955 and 2020
slide5 = Slide()


# Step 1 - switch back to value instead of percentage
slide5.add_step(Step(Config({"align": "none"})))
# Step 2 - switch to a stacked column chart by changing the geometry
slide5.add_step(
    Step(
        Config(
            {
                "geometry": "rectangle",
            }
        )
    )
)
# Step 2 - zoom to data from the first and last years
slide5.add_step(
    Step(
        Data.filter("record.Year === '1955' || record.Year === '2020' "),
        Config(
            {
                "title": "Zoom to Specific Elements",
            }
        ),
    ),
)
story.add_slide(slide5)

# Group & rearrange elements for comparison
slide6 = Slide()
slide6.add_step(
    Step(
        Config(
            {
                "x": ["Year", "Function"],
                "y": "Amount[B$]",
                "label": "Amount[B$]",
                "title": "Group & Rearrange for Better Comparison",
            }
        )
    )
)

slide6.add_step(Step(Config({"x": ["Function", "Year"]})))
story.add_slide(slide6)


# Switch on the tooltip that appears
# when the user hovers the mouse over a chart element.
story.set_feature("tooltip", True)

# Set a handler that prevents showing the year values that are not divisible by 5
handler = """
let Year = parseFloat(event.data.text);
if (!isNaN(Year) && Year > 1950 && Year < 2020 && Year % 5 !== 0) {
    event.preventDefault();
}
"""
# Add handler to the plot-axis-label-draw event so that it takes effect.
story.add_event("plot-axis-label-draw", handler)

# Play the created story
story.play()
