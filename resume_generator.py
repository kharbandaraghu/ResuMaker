# resume_generator.py
import yaml
import re
import subprocess

def parse_text(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', text)
    return text.replace('%', '\\%')

def yaml_to_latex(yaml_file, latex_template_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)

    # Read the LaTeX template
    with open(latex_template_file, 'r') as file:
        latex_template = file.read()

    # Replace placeholders in the template with data from YAML
    latex_content = latex_template

    # Personal Information
    name = data['name']
    email = data['email']
    phone = data['phone']
    linkedin_text = data['linkedin']['text']
    linkedin_url = data['linkedin']['url']

    header = f"""
    \\begin{{center}}
        \\textbf{{{{\\Huge \\scshape {name}}}}} \\\\ \\vspace{{1pt}}
        \\small {phone} $|$ \\href{{{{mailto:{email}}}}}{{{{\\underline{{{{{email}}}}}}}}} $|$ 
        \\href{{{{{linkedin_url}}}}}{{{{\\underline{{{{{linkedin_text}}}}}}}}}
    \\end{{center}}
    """

    latex_content = latex_content.replace('%HEADER%', header)

    # Summary of Qualifications
    summary_items = ''
    for item in data['summary_of_qualifications']:
        item = parse_text(item)
        summary_items += f'\\resumeItem{{{item}}}\n'
    summary = f"""
    \\section{{Summary of Qualifications}}
    \\begin{{itemize}}[leftmargin=0.15in, label={{}}]
        \\small{{{{\\item{{
            {summary_items}
        }}}}}}
    \\end{{itemize}}
    """
    latex_content = latex_content.replace('%SUMMARY%', summary)

    # Experience
    experience_entries = ''
    for job in data['experience']:
        company = job['company']
        position = job['position']
        location = job['location']
        dates = job['dates']
        responsibilities = ''
        for resp in job['responsibilities']:
            resp = parse_text(resp)
            responsibilities += f'\\resumeItem{{{resp}}}\n'
        experience_entry = f"""
        \\resumeSubheading
          {{{{{position}}}}}{{{dates}}}
          {{{{{company}}}}}{{{location}}}
          \\resumeItemListStart
            {responsibilities}
          \\resumeItemListEnd
        """
        experience_entries += experience_entry

    experience_section = f"""
    \\section{{Experience}}
      \\resumeSubHeadingListStart
        {experience_entries}
      \\resumeSubHeadingListEnd
    """
    latex_content = latex_content.replace('%EXPERIENCE%', experience_section)

    # Projects
    project_entries = ''
    for project in data['projects']:
        title = parse_text(project['title'])
        technologies = parse_text(project['technologies'])
        descriptions = ''
        for desc in project['description']:
            desc = parse_text(desc)
            descriptions += f'\\resumeItem{{{desc}}}\n'
        project_entry = f"""
        \\resumeProjectHeading
            {{{{\\textbf{{{title}}} $|$ \\emph{{{technologies}}}}}}}{{}}
            \\resumeItemListStart
              {descriptions}
            \\resumeItemListEnd
        """
        project_entries += project_entry

    projects_section = f"""
    \\section{{Projects}}
      \\resumeSubHeadingListStart
        {project_entries}
      \\resumeSubHeadingListEnd
    """
    latex_content = latex_content.replace('%PROJECTS%', projects_section)

    # Education
    education_entries = ''
    for edu in data['education']:
        school = edu['school']
        degree = edu['degree']
        location = edu['location']
        dates = edu['dates']
        courses = edu.get('courses', '')
        education_entry = f"""
        \\resumeSubheading
          {{{{{school}}}}}{{{location}}}
          {{{{{degree}}}}}{{{dates}}}
          \\resumeItemListStart
            \\resumeItem{{\\textbf{{Relevant Courses}}: {courses}}}
          \\resumeItemListEnd
        """
        education_entries += education_entry

    education_section = f"""
    \\section{{Education}}
      \\resumeSubHeadingListStart
        {education_entries}
      \\resumeSubHeadingListEnd
    """
    latex_content = latex_content.replace('%EDUCATION%', education_section)

    # Certifications
    cert_items = ''
    for cert in data['certifications']:
        cert = parse_text(cert)
        cert_items += f'{cert} \\\\\n'
    certifications_section = f"""
    \\section{{Certifications}}
    \\begin{{itemize}}[leftmargin=0.15in, label={{}}]
        \\small{{{{\\item{{
            {cert_items}
        }}}}}}
    \\end{{itemize}}
    """
    latex_content = latex_content.replace('%CERTIFICATIONS%', certifications_section)

    # Technical Skills
    skills = data['technical_skills']
    skills_entries = f"""
    \\textbf{{Programming Languages}}{{: {skills['programming_languages']}}} \\\\
    \\textbf{{Frameworks \\& Technologies}}{{: {skills['frameworks_and_technologies']}}} \\\\
    \\textbf{{Databases}}{{: {skills['databases']}}} \\\\
    \\textbf{{Tools}}{{: {skills['tools']}}} \\\\
    \\textbf{{Cloud Platforms}}{{: {skills['cloud_platforms']}}}
    """
    technical_skills_section = f"""
    \\section{{Technical Skills}}
     \\begin{{itemize}}[leftmargin=0.15in, label={{}}]
        \\small{{{{\\item{{
         {skills_entries}
        }}}}}}
     \\end{{itemize}}
    """
    latex_content = latex_content.replace('%TECHNICAL_SKILLS%', technical_skills_section)

    return latex_content

def latex_to_pdf(latex_code, output_pdf='resume.pdf'):
    with open('resume.tex', 'w') as f:
        f.write(latex_code)

    # Compile LaTeX to PDF using pdflatex
    # subprocess.run(['pdflatex', '-interaction=nonstopmode', 'resume.tex'])
    # subprocess.run(['pdflatex', '-interaction=nonstopmode', 'resume.tex'])  # Run twice for TOC

    # Rename the generated PDF to the desired output file name
    # subprocess.run(['mv', 'resume.pdf', output_pdf])

# Main execution
if __name__ == '__main__':
    latex_code = yaml_to_latex('tmp/resume.yaml', 'resume_template.tex')
    latex_to_pdf(latex_code)
