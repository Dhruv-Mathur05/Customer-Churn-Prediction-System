from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer)
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

#create the function 
def create_pdf(report_data, prediction, confidence, recommendations, loyal):
    #pdf creater(creates an empty pdf)
    doc = SimpleDocTemplate(
        "Customer_Churn_Report.pdf"
    )
    styles = getSampleStyleSheet() #styles
    story = []

    #add title
    story.append(
        Paragraph(
            '<b>Customer Churn Prediction Report </b>', styles['Title']
        ))
    
    #Customer Details
    story.append(
        Paragraph(
            '<b>Customer Details </b>', styles['Heading2']
        ))

    for key,value in report_data.items():
        story.append(
            Paragraph(
                f'{key}: {value}',
                styles['BodyText']
            )
        )

    #Prediction
    story.append(Spacer(1,20))
    prediction_text = (
        'Customer is likely to Stay' 
        if prediction == 0
        else 'Customer is likely to Leave'
    )
    story.append(
        Paragraph(
            '<b>Prediction</b>', styles['Heading2']
        ))
    story.append(
        Paragraph(
            prediction_text, styles['BodyText']
        ))
    
    #Confidence
    story.append(
        Paragraph(
            f'Confidence : {confidence:.2f}%', styles['BodyText']
        ))

    #Recommendations
    story.append(Spacer(1,20))
    if prediction == 1:
        story.append(
            Paragraph(
                '<b>Recommendations</b>', styles['Heading2']
            ))
        for rec in recommendations:
            story.append(
                Paragraph(
                    f'~ {rec}',
                    styles['BodyText']
                ))
    else:
        story.append(
            Paragraph(
                f'{loyal}', styles['BodyText']
            ))

    #Footer
    story.append(Spacer(1,20))
    story.append(
        Paragraph(
            'Generated using Customer churn Prediction System',
            styles['Italic']
        ))
    story.append(
        Paragraph(
            'Developed by <b>Dhruv Mathur</b>', styles['Italic']
        ))

    current_time = datetime.now().strftime('%d-%m-%Y %H:%M')
    story.append(
        Paragraph(
            f'Report Generated on: {current_time}', styles['Italic']
        ))
    story.append(
        Paragraph(
            'Thank you for using this application!', styles['Italic']
        ))

    doc.build(story)