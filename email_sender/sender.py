from django.template import loader, Context
from django.core.mail import EmailMessage

from crossfit.email_sender.models import UserEmailPermissions

def email_user(user, subject, email_template, data_dict):

    # Manually create the template and context, then render the result
    t = loader.get_template(email_template)
    c = Context(data_dict)
    html_content = t.render(c)

    # TODO : Register a better username
    from_email   = "owenmead_server@owenmead.webfactional.com"
    to_address = [user.email]

    # Create the actual message
    msg = EmailMessage(subject, html_content, from_email, to_address)
    msg.content_subtype = "html"  # Mark the email as an HTML email
    msg.send()
