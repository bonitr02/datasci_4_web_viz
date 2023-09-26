# Import necessary libraries
library(shiny)
library(ggplot2)
library(dplyr)
library(rsconnect)

# UI for the Shiny app
ui <- fluidPage(
  titlePanel("All Teeth Lost in NY, CA and FL by Age-adjusted Prevalence"),
  sidebarLayout(
    sidebarPanel(
      selectInput("state", "Choose a state:", choices = NULL)
    ),
    mainPanel(
      plotOutput("barPlot")
    )
  )
)


# Server logic
server <- function(input, output, session) {
  
  # Load the dataset
  df <- reactive({
    url <- "https://raw.githubusercontent.com/bonitr02/datasci_4_web_viz/main/HEALTHYPLACES__Local_Data_for_Better_Health__County_Data_2023_release.csv"
    read.csv(url)
  })
  
  # Filter the dataset
  df_teeth <- reactive({
    data <- df()
    filter(data, MeasureId == "TEETHLOST", Data_Value_Type == "Age-adjusted prevalence")
  })
  
  # Update state choices dynamically based on dataset
  observe({
    teeth_data <- df_teeth()
    updateSelectInput(session, "state", choices = sort(unique(teeth_data$StateDesc)))
  })
  
  # Render the bar plot
  output$barPlot <- renderPlot({
    teeth_data <- df_teeth()
    state_data <- teeth_data[teeth_data$StateDesc == input$state, ]
    avg_value <- mean(teeth_data$Data_Value, na.rm = TRUE)
    
    ggplot() +
      geom_bar(data = state_data, aes(x = StateDesc, y = Data_Value, fill = StateDesc), stat = "identity") +
      geom_hline(aes(yintercept = avg_value), linetype = "dashed", color = "dodgerblue") +
      labs(title = 'All Teeth Lost in NY, CA and FL by Age-adjusted Prevalence',
           y = 'Data Value (Age-adjusted prevalence) - Percent',
           x = 'Location (State)') +
      theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
      ylim(0, 30) +
      scale_fill_manual(values = c("cyan1", "aquamarine1"))
  })
  
}

# Run the Shiny app
shinyApp(ui, server)

#rsconnect::setAccountInfo(name="fh0bjx-bonitr02", token="A2991CA8526CB8B9C87CF89D362C9F50", secret="1l5C9EkwdFmEU3o2Xqk00xioH3ZkvCxzuA4xzzHt")
#deployApp()
