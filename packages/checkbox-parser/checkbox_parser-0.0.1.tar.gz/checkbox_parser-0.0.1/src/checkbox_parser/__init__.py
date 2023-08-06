import json
import uuid


class html_parser:

  def __init__(self, body):
      self.body = body


  def sort_questions(self, data):
    sorted_questions = sorted(data, key=lambda s: s["position"])
    return sorted_questions


  def wrapper(self, questions):
    html_elements = list()


    for question_data in questions:
      quest_elem = list()

      html_question = f"<p class='lead text-center' style='font-size: 28px';>{question_data['question']}</p>"
      quest_elem.append(html_question)
      id_question = str(question_data["id_question"])

      for answer in question_data["answers"]:

        uid = str(uuid.uuid4())
        uid = uid.split("-")[0]

        answer_formated = answer.replace(" ", "_")
        input_html = f"<input class='form-check-input' type='checkbox'  id='{answer_formated}-{id_question}-{uid}' name='group1'>"
        label_html = f"<label class='form-check-label' style='font-size: 20px;' for='{answer_formated}-{id_question}-{uid}'>{answer}</label><br>"

        quest_elem.append([input_html, label_html])

      html_elements.append(quest_elem)

    return html_elements

  def tag_maker(self, list):
      html_element = ""
      for questions_answes in list:

          initial_fieldset = "<fieldset>"
          last_fieldset = "</fieldset>"

          html_element = html_element+initial_fieldset
          html_element = html_element+questions_answes[0]
          questions_answes.pop(0)
          for element in questions_answes:

              initial_div = "<div class='form-check text-center'>"
              last_div = "</div>"

              html_element = html_element+initial_div
              html_element = html_element+element[0]
              html_element = html_element+element[1]
              html_element = html_element+last_div

          html_element = html_element+last_fieldset
      return html_element


  def get_html(self):
    questions = self.sort_questions(self.body)
    return self.tag_maker(self.wrapper(questions))


