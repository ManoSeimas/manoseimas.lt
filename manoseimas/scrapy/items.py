from six import text_type
from scrapy.contrib.loader import processor
from scrapy.item import Field
from scrapy.item import Item
from scrapy.utils.python import unique

from .loaders import absolute_url


"""
ID suffixes:

    p - person

    q - question

    d - document

    v - voting

"""


class Source(Item):
    id = Field()
    url = Field()
    name = Field()


class Person(Item):
    _id = Field()
    first_name = Field()
    last_name = Field()
    dob = Field()
    email = Field(output_processor=unique)
    phone = Field(output_processor=unique)
    home_page = Field(output_processor=absolute_url)
    candidate_page = Field()
    raised_by = Field()
    photo = Field()
    image_urls = Field(output_processor=processor.Identity())
    images = Field(output_processor=processor.Identity())
    office_address = Field()
    parliament = Field(output_processor=unique)
    constituency = Field()
    party_candidate = Field()
    groups = Field(input_processor=processor.Identity(),
                   output_processor=processor.Identity())
    source = Field(input_processor=processor.Identity(),
                   output_processor=processor.TakeFirst())
    _attachments = Field(input_processor=processor.Identity(),
                         output_processor=processor.Identity())
    biography = Field()


class Group(Item):
    type = Field(input_processor=processor.Identity())
    name = Field()
    membership = Field(input_processor=processor.Identity(),
                       output_processor=processor.Identity())
    position = Field()
    source = Field(output_processor=absolute_url)


class Question(Item):
    _id = Field()
    name = Field()
    speakers = Field(input_processor=processor.Identity(),
                     output_processor=processor.Identity())
    session = Field(input_processor=processor.Identity(),
                    output_processor=processor.TakeFirst())
    formulation = Field()
    documents = Field(input_processor=processor.Identity(),
                      output_processor=processor.Identity())
    source = Field(input_processor=processor.Identity(),
                   output_processor=processor.TakeFirst())


class QuestionDocument(Item):
    id = Field()
    name = Field()
    type = Field()
    number = Field()
    speakers = Field(input_processor=processor.Identity(),
                     output_processor=processor.Identity())


class QuestionDocumentSpeaker(Item):
    name = Field()
    position = Field()
    committee = Field()
    institution = Field()


class DocumentInvolved(Item):
    date = Field()
    how = Field()
    person = Field()
    committee = Field()
    group = Field()
    group_type = Field()
    institution = Field()


class Document(Item):
    _id = Field()
    name = Field()
    type = Field(input_processor=processor.MapCompose(text_type.strip,
                                                      text_type.lower))
    number = Field()
    date = Field()
    language = Field()
    by = Field(input_processor=processor.Identity(),
               output_processor=processor.Identity())
    source = Field(input_processor=processor.Identity(),
                   output_processor=processor.TakeFirst())


class LegalAct(Item):
    _id = Field()
    name = Field()
    kind = Field(input_processor=processor.MapCompose(text_type.strip,
                                                      text_type.lower))
    number = Field()
    date = Field()
    relations = Field(input_processor=processor.Identity(),
                      output_processor=processor.TakeFirst())
    involved = Field(input_processor=processor.Identity(),
                     output_processor=processor.Identity())
    source = Field(input_processor=processor.Identity(),
                   output_processor=processor.TakeFirst())

    _attachments = Field(input_processor=processor.Identity(),
                         output_processor=processor.Identity())


class Session(Item):
    id = Field()
    fakt_pos_id = Field()
    number = Field()
    date = Field()
    type = Field()


class Voting(Item):
    _id = Field()
    type = Field()
    name = Field()
    documents = Field(input_processor=processor.Identity(),
                      output_processor=processor.Identity())
    datetime = Field()
    vote_aye = Field()
    vote_no = Field()
    vote_abstain = Field()
    no_vote = Field()
    total_votes = Field()
    votes = Field(input_processor=processor.Identity(),
                  output_processor=processor.Identity())
    formulation = Field()
    formulation_a = Field()
    formulation_b = Field()
    result = Field()
    question = Field()
    # documents = Field(output_processor=processor.Identity())
    registration = Field(input_processor=processor.Identity(),
                         output_processor=processor.TakeFirst())
    source = Field(input_processor=processor.Identity(),
                   output_processor=processor.TakeFirst())


class VotingDocument(Item):
    id = Field()
    name = Field()
    type = Field()
    number = Field()


class PersonVote(Item):
    name = Field()
    person = Field()
    fraction = Field()
    vote = Field()


class Registration(Item):
    id = Field()
    datetime = Field()
    joined = Field()


class StenogramTopic(Item):
    _id = Field()
    date = Field(input_processor=processor.Identity(),
                 output_processor=processor.TakeFirst())
    title = Field()
    sitting_no = Field()
    sitting_name = Field()

    session = Field(input_processor=processor.Identity(),
                    output_processor=processor.TakeFirst())

    source = Field(input_processor=processor.Identity(),
                   output_processor=processor.TakeFirst())
    statements = Field(input_processor=processor.Identity(),
                       output_processor=processor.Identity())


class ProposedLawProjectProposer(Item):
    id = Field()
    date = Field(input_processor=processor.Identity(),
                 output_processor=processor.TakeFirst())
    proposer_name = Field()
    project_name = Field()
    project_number = Field()
    project_url = Field()
    passed = Field(input_processor=processor.Identity(),
                   output_processor=processor.TakeFirst())
    source = Field(input_processor=processor.Identity(),
                   output_processor=processor.TakeFirst())


class PassedLawProjectProposer(Item):
    id = Field()
    passing_date = Field(input_processor=processor.Identity(),
                         output_processor=processor.TakeFirst())
    proposer_name = Field()
    passing_number = Field()
    passing_url = Field()
    source = Field(input_processor=processor.Identity(),
                   output_processor=processor.TakeFirst())


class Lobbyist(Item):
    name = Field(output_processor=processor.TakeFirst())
    url = Field()
    representatives = Field()
    company_code = Field()
    date_of_inclusion = Field(input_processor=processor.Identity(),
                              output_processor=processor.TakeFirst())
    decision = Field()
    status = Field()
    source_url = Field()
    raw_data = Field()


class LobbyistDeclaration(Item):
    name = Field()
    year = Field()
    comments = Field()
    clients = Field(input_processor=processor.Identity(),
                    output_processor=processor.Identity())
    law_projects = Field(output_processor=processor.Identity())
    source_url = Field()
    raw_data = Field()


class LobbyistClient(Item):
    client = Field()
    law_projects = Field(output_processor=processor.Identity())


class Suggestion(Item):
    submitter = Field()
    date = Field()
    document = Field()
    opinion = Field()
    source_url = Field()
    source_id = Field()
    source_index = Field()
    raw = Field()
