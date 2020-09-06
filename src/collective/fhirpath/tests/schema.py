# _*_ coding: utf-8 _*_
from plone.app.fhirfield import FhirResource
from plone.dexterity.content import Container
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer


__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


class IOrganization(model.Schema):
    """ """

    organization_resource = FhirResource(
        title=u"Fhir Organization Field",
        fhir_release="STU3",
        model="fhir.resources.STU3.organization.Organization",
    )


@implementer(IOrganization)
class Organization(Container):
    """ """

    def get_resource(self):
        """ """
        return IOrganization["organization_resource"].get(self)


class IPatient(model.Schema):
    """ """

    patient_resource = FhirResource(
        title=u"Fhir Patient Field",
        fhir_release="STU3",
        model="fhir.resources.STU3.patient.Patient",
    )


@implementer(IPatient)
class Patient(Container):
    """ """

    def get_resource(self):
        """ """
        return IPatient["patient_resource"].get(self)


class IPractitioner(model.Schema):
    """ """

    practitioner_resource = FhirResource(
        title=u"Fhir Practitioner Field",
        fhir_release="STU3",
        model="fhir.resources.STU3.practitioner.Practitioner",
    )


@implementer(IPractitioner)
class Practitioner(Container):
    """ """

    def get_resource(self):
        """ """
        return IPractitioner["practitioner_resource"].get(self)


class IQuestionnaire(model.Schema):
    """ """

    questionnaire_resource = FhirResource(
        title=u"Fhir Questionnaire Field",
        fhir_release="STU3",
        model="fhir.resources.STU3.questionnaire.Questionnaire",
    )


@implementer(IQuestionnaire)
class Questionnaire(Container):
    """ """

    def get_resource(self):
        """ """
        return IQuestionnaire["questionnaire_resource"].get(self)


class IQuestionnaireResponse(model.Schema):
    """ """

    questionnaireresponse_resource = FhirResource(
        title=u"Fhir QuestionnaireResponse Field",
        fhir_release="STU3",
        model="fhir.resources.STU3.questionnaireresponse.QuestionnaireResponse",
    )


@implementer(IQuestionnaireResponse)
class QuestionnaireResponse(Container):
    """ """

    def get_resource(self):
        """ """
        return IQuestionnaireResponse["questionnaireresponse_resource"].get(self)


class ITask(model.Schema):
    """ """

    task_resource = FhirResource(
        title=u"Fhir Task Field",
        fhir_release="STU3",
        model="fhir.resources.STU3.task.Task",
    )


@implementer(ITask)
class Task(Item):
    """ """

    def get_resource(self):
        """ """
        return ITask["task_resource"].get(self)


class IProcedureRequest(model.Schema):
    """ """

    procedurerequest_resource = FhirResource(
        title=u"Fhir ProcedureRequest Field",
        fhir_release="STU3",
        model="fhir.resources.STU3.procedurerequest.ProcedureRequest",
    )


@implementer(IProcedureRequest)
class ProcedureRequest(Item):
    """ """

    def get_resource(self):
        """ """
        return IProcedureRequest["procedurerequest_resource"].get(self)


class IDevice(model.Schema):
    """ """

    device_resource = FhirResource(
        title=u"Fhir Device Field", fhir_release="STU3", resource_type="Device"
    )


@implementer(IDevice)
class Device(Item):
    """ """

    def get_resource(self):
        """ """
        return IDevice["device_resource"].get(self)


class IDeviceRequest(model.Schema):
    """ """

    devicerequest_resource = FhirResource(
        title=u"Fhir DeviceRequest Field",
        fhir_release="STU3",
        resource_type="DeviceRequest",
    )


@implementer(IDeviceRequest)
class DeviceRequest(Item):
    """ """

    def get_resource(self):
        """ """
        return IDeviceRequest["devicerequest_resource"].get(self)


class IValueSet(model.Schema):
    """ """

    valueset_resource = FhirResource(
        title=u"Fhir ValueSet Field", fhir_release="STU3", resource_type="ValueSet"
    )


@implementer(IValueSet)
class ValueSet(Item):
    """ """

    def get_resource(self):
        """ """
        return IValueSet["valueset_resource"].get(self)


class IChargeItem(model.Schema):
    """"""

    chargeitem_resource = FhirResource(
        title=u"Fhir ChargeItem Field", fhir_release="STU3", resource_type="ChargeItem"
    )


@implementer(IChargeItem)
class ChargeItem(Item):
    """ """

    def get_resource(self):
        """ """
        return IChargeItem["chargeitem_resource"].get(self)


class IEncounter(model.Schema):
    """"""

    encounter_resource = FhirResource(
        title=u"Fhir FFEncounter Field", fhir_release="STU3", resource_type="Encounter"
    )


@implementer(IEncounter)
class Encounter(Item):
    """ """

    def get_resource(self):
        """ """
        return IEncounter["encounter_resource"].get(self)


class IMedicationRequest(model.Schema):
    """"""

    medicationrequest_resource = FhirResource(
        title=u"Fhir MedicationRequest Field",
        fhir_release="STU3",
        resource_type="MedicationRequest",
    )


@implementer(IMedicationRequest)
class MedicationRequest(Item):
    """ """

    def get_resource(self):
        """ """
        return IMedicationRequest["medicationrequest_resource"].get(self)


class IObservation(model.Schema):
    """"""

    observation_resource = FhirResource(
        title=u"Fhir Observation Field",
        fhir_release="STU3",
        resource_type="Observation",
    )


@implementer(IObservation)
class Observation(Item):
    """ """

    def get_resource(self):
        """ """
        return IObservation["observation_resource"].get(self)


class IMedia(model.Schema):
    """"""

    media_resource = FhirResource(
        title=u"Fhir Media Field", fhir_release="STU3", resource_type="Media"
    )


@implementer(IMedia)
class Media(Item):
    """ """

    def get_resource(self):
        """ """
        return IMedia["media_resource"].get(self)
