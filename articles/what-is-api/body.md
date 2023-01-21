The word “API” is getting thrown around a lot lately, and increasingly so in non-technical contexts. 
Between _“the `<x>` API is down”_, _“my graphics card has the `<y>` API”_, or _“`<z>` API needs authentication”_,
it can all get rather confusing. So… let’s de-mystify this API business a bit.

----------

## The actual definition of "API"

That’s easy! Just check [Wikipedia](https://en.wikipedia.org/wiki/API):

> In computer programming, an application programming interface (API) is a set of routines, protocols, and tools
> for building software and applications.
> 
> An API expresses a software component in terms of its operations, inputs, outputs, and underlying types, defining 
> functionalities that are independent of their respective implementations, which allows definitions and implementations
> to vary without compromising the interface. A good API makes it easier to develop a program by providing all the
> building blocks, which are then put together by the programmer.

If that did not totally explain it for you, don’t fret. The API is one of those concepts that is intuitive, but requires a lot of words to define. To understand what the definition is getting at, let’s look at a real world parallel:

## The “postal service” API

:::imagecard right letter.webp
:::

Suppose you work as a clerk at a university. It’s graduation time, and you must somehow deliver the new graduates’ diplomas to their recipients. The most straightforward way to do this is to put the diplomas in a big bag, then go find the students to give them their respective diplomas. Simple, right?

Well, no. That would be an awfully time-consuming and ineffective task. Instead, why not mail it to them? There’s a well-defined process for that:

1. Put the paper to send (in this case, the diploma) in an envelope.
2. Write your name and address on the top left of the envelope.
3. Write your recipient’s name and address in the center of the envelope.
4. Place an appropriate stamp on the top right corner of the envelope.
5. Drop the envelope into your local mailbox.

If you follow these steps, you trigger a long chain of events and processes that has one ultimate outcome: the student receives their diploma. This is courtesy to your local postal service, which publishes other sets of instructions for different sorts of outcomes: delivering non-paper stuff (packages), delivering stuff more quickly, confirming the mail reached its destination, and even insuring the delivery.

At the same time you are using the postal service to mail these diplomas, other people are using the same postal service with the same sets of instructions to move their stuff around. Nobody actually cares how the stuff happens; whether the mail makes it there by truck, boat, or plane doesn’t matter. All you and the other users care is that if you follow the instructions, a given outcome will happen.

As a whole, the postal service (and all its defined procedures and outcomes) is an API for sending mail:

> An API expresses **a real life service** in terms of its operations, inputs, outputs, and underlying types, defining functionalities that are independent of their respective implementations, which allows definitions and implementations to vary without compromising the interface. A good API makes it easier **to do stuff** by providing all the building blocks, which are then put together by the **person doing it**.

:::imagecard center usps.webp
Your local friendly API service, come rain or shine, snow or sleet.
:::

## Back in the digital realm...

So how does this compare to APIs in the computer programming sense? Very directly, actually! Suppose we’re trying to send an e-mail congratulating a student on graduating using Python. Python defines an API to do this — a set of instructions and tools in the `email` and `smtplib` packages. Just like the list above, the [recommended](https://docs.python.org/3/library/email-examples.html) steps to send an e-mail are:

```python
from email.mime.text import MIMEText
from smtplib import SMTP

message = MIMEText("Congratulations, Studious Student, on graduating from Example University! You are truly a star student!")
message["From"] = "no-reply@example.edu"
message["To"] = "studious.student@example.com"
message["Subject"] = "Salutations, grad!"

connection = SMTP("127.0.0.1")
connection.send_message(message)
connection.quit()
```

In short, the steps are: fetch the tools, build a message (with its from/to/subject parts), then send it using SMTP (Simple Mail Transfer Protocol) to the IP address `127.0.0.1`.

Just as there are a ton of complex steps to sending a real letter, there is a bunch of stuff that the instructions above causes to happen, but what it is doesn’t matter. All that matters is that the student gets their message.

## APIs in different forms

As you may have noticed, the term “API” is a rather broad one. It really can apply to a variety of things:

* Sending email using Python’s `email`/`smtplib`
* Interacting with Reddit by sending queries to its web API: `https://api.reddit.com`
* Controlling your graphics card using the DirectX or OpenGL collections of instructions (APIs)
* Manipulating elements on a webpage in Javascript using the jQuery API

There can be multiple APIs to do the same thing (like DirectX and OpenGL), or APIs that use other APIs in order to add more features and make them easier to use, like the Python [PRAW library](https://praw.readthedocs.org/en/stable/), which simplifies interacting with Reddit by letting the developer not care about the “web” aspect.

:::imagecard center i-herd-u-liek-apis.webp
:::

## Wrapping up

Finally, let’s take a look at those confusing statements from the start of this post, and see if we don’t have some further understanding of them:

* _“The `<x>` API is down”_ — these tools require a server somewhere to be working, and it is currently broken

* _“My graphics card has the `<y>` API”_ — to control my graphics card, use that set of tools and it will understand you
  
* _“`<z>` API needs authentication”_ — those tools need whoever is using them to identify themselves in some way

That’s it! I hope this maybe clarifies any confusion around what “API” means in a general sense.

:::alert success
This post was [originally published on my Medium blog](https://medium.com/@fsufitch/what-is-this-api-thing-3b22bcb94d53).
:::
