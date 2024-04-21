import os
from Packages.ResuMaker import ResumeMaker as rm, Run, TextStyle, ParagraphStyle
import json
from docx2pdf import convert
import argparse

# Get the current script directory
script_dir = os.path.dirname(os.path.realpath(__file__))

# Create the parser
parser = argparse.ArgumentParser()
# Add arguments
parser.add_argument('-bfs', '--base-font-size', type=float, default=10.5, help='Base font size')
parser.add_argument('-ff', '--font-family', default='GoogleSans', help='Font family')
parser.add_argument('-bls', '--bullet-line-spacing', type=float, default=1.0, help='Bullet line spacing')
parser.add_argument('-o', '--output-file', default='resume.pdf', help='Output file name')

# Parse the arguments
args = parser.parse_args()

# Access the values
base_font_size = args.base_font_size
font_family = args.font_family
bullet_line_spacing = args.bullet_line_spacing
output_file = args.output_file

# Load data from resumeData.yaml
with open(os.path.join(script_dir, 'tmp', 'resumeData.json'), 'r') as resume_file:
    resume_data = json.load(resume_file)

# initialize object
resume = rm(margins=[0.25, 0.25, 0.25, 0.25])

# for name heading
h1 = TextStyle(font_size=base_font_size * 1.8, font_name=font_family, font_color=(0,51,102))
p1 = ParagraphStyle(align='center')

# for contact
ts_contact = TextStyle(font_size=base_font_size * 0.9, font_name=f'{font_family}-Medium')
ts_contact_hyperlink = TextStyle(font_size=base_font_size * 0.9, font_name=f'{font_family}-Medium', isHyperlink=True, 
                                 url=resume_data['linkedin']['linkedin-url'], font_color=(0,51,102), underline=True)
p_contact = ParagraphStyle(align='center')

# For subheadings like experience, summary etc.
h2 = TextStyle(font_name=f'{font_family}-Medium', font_size=base_font_size * 1.3)
p2 = ParagraphStyle(style='Title', space_before=base_font_size * 0.5)

# for sub sub headings like job names or school name
h3 = TextStyle(font_size=base_font_size * 1.2, font_name=f'{font_family}-Medium', font_color=(0,102,204))
p3 = ParagraphStyle(space_before=base_font_size * 0.5)

# for work experience right after role para
p4 = ParagraphStyle(space_after=base_font_size * 0.25)

# special p - for skills and projects headings also contains space after
psp = ParagraphStyle(style='Title', space_before=base_font_size * 0.5, space_after=base_font_size * 0.25)

# generic styles
bulletText = TextStyle(font_size=base_font_size)
bulletPara = ParagraphStyle(style='List Bullet', indent_level=0.5, line_spacing=bullet_line_spacing)
normalText = TextStyle(font_size=base_font_size)
normalPara = ParagraphStyle(line_spacing=1.1)
boldText = TextStyle(font_size=base_font_size, font_name=f'{font_family}-Bold')
italicText = TextStyle(font_size=base_font_size, font_name=f'{font_family}-Italic')

# Name and Heading
resume.addMultipleText([Run(resume_data['name'], h1)], p1)

# Contact Information
contact_info = [
    Run(resume_data['email'], ts_contact),
    Run(' | ', ts_contact),
    Run(resume_data['phone'], ts_contact),
    Run(' | ', ts_contact),
    Run(resume_data['linkedin']['linkedin-text'], ts_contact_hyperlink),
]
resume.addMultipleText(contact_info, p_contact)

# Skills
resume.addMultipleText([Run("Skills", h2)], psp)
for skill in resume_data['skills']:
    line = [
        Run(skill['name']+": ", boldText),
        Run(skill['value'], normalText)    
    ]
    resume.addMultipleText(line, bulletPara)

# Experience
resume.addMultipleText([Run("Work Experience", h2)], p2)
for experience in resume_data['work-experience']:
    resume.addLeftRightText(Run(experience['company'], h3), Run(experience['location'], normalText), p3)
    resume.addLeftRightText(Run(experience['role'], boldText), Run(experience['duration'], italicText), p4)
    for bullet in experience['responsibilities']:
        resume.addMultipleText([Run(bullet, bulletText)], bulletPara)

# Projects
resume.addMultipleText([Run("Projects", h2)], psp)
for project in resume_data['projects']:
    resume.addMultipleText([Run(project['name'], boldText)], normalPara)
    resume.addMultipleText([Run(project['description'], normalText)], normalPara)

# Education
resume.addMultipleText([Run("Education", h2)], p2)
for education in resume_data['education']:
    resume.addLeftRightText(Run(education['school'], h3), Run(education['location'], normalText), p3)
    resume.addLeftRightText(Run(education['degree'], boldText), Run(education['duration'], italicText), normalPara)
    resume.addMultipleText([Run("Courses:", boldText) , Run(education['courses'], normalText)], bulletPara)

resume.save(os.path.join(script_dir, 'tmp', 'Resume.docx'))
# save as pdf
convert(os.path.join(script_dir, 'tmp', 'Resume.docx'), os.path.join(script_dir, output_file))
