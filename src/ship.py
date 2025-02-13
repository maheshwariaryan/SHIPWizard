import os
from fastapi import FastAPI
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process
import uvicorn
from dotenv import load_dotenv
 
app = FastAPI()

load_dotenv()
api_key = os.getenv("API_KEY")
api_base = os.getenv("OPENAI_API_BASE")
api_model_name = os.getenv("OPENAI_MODEL_NAME")
 
# OpenAI (Groq) API Configuration
os.environ["OPENAI_API_BASE"] = api_base
os.environ["OPENAI_MODEL_NAME"] = api_model_name
os.environ["OPENAI_API_KEY"] = api_key

class input(BaseModel):
    content: str
 
@app.post("/category/")
async def extract_details(content: input):
        
        pdf = """
        DEFINITIONS
The following words and phrases, if used in this Plan, will have the following meanings. Any
services, treatment or supplies not specifically listed in this Plan Document as Eligible Expenses
are not covered by this Plan.
Accident refers to an occurrence which (a) is unforeseen; (b) is not due to or contributed to by
Illness or disease of any kind; and (c) causes Injury.
Activities of Daily Living are the day-to-day activities, such as continence, dressing, feeding,
toileting and transferring.
Administrator or Plan Administrator means the fiduciary named in this Plan.
Alcoholism is the condition caused by regular excessive compulsive drinking of alcohol that
results in a chronic disorder affecting physical health and/or personal or social functioning.
Ambulance is a specially designed vehicle transporting the sick or injured that contains a
stretcher, linens, first aid supplies, oxygen equipment and other life saving equipment required by
the state and local law and that is staffed by personnel trained to provide first aid treatment.
Ambulatory Surgical Center is a licensed facility that is used mainly for performing outpatient
surgery, has a staff of Physicians, has continuous Physician and nursing care by Registered
Nurses (R.N.’s) and does not provide for overnight stays.
Amendment is the formal process and resulting document that changes the provisions of the
Plan Document, duly signed by the authorized person(s) as designated by the Plan Administrator.
Area means a county or larger geographic area, if a larger area is required, needed to obtain a
representative level of Usual, Customary and Reasonable (UCR) charges.
Baseline shall mean the initial test results to which the results in future years will be compared in
order to detect abnormalities.
Birthing Center means a facility licensed in the state where operating which is equipped and
operating solely to provide prenatal and post-partum care in connection with spontaneous
deliveries, which includes:
1. The direction by at least one Physician specializing in obstetrics and gynecology,
2. The presence of a Physician or nurse midwife during each birth and immediate post-partum
period,
3. The presence of full-time skilled nursing services in the delivery rooms and recovery rooms
under the direction of a Registered Nurse (R.N.) or nurse midwife,
4. The extension of staff privileges to Physicians who provide obstetrical and gynecological care
in an area hospital,
5. At least two beds or birthing rooms for patients during labor and delivery,
6. Diagnostic x-ray, testing and laboratory equipment (or a contract to use such equipment at an
area hospital),
5

DEFINITIONS
Birthing Center, (continued)
7. Equipment and supplies for administration of local anesthetic for performing minor surgical
procedures and medical emergencies (including oxygen and resuscitation equipment,
intravenous fluids and drugs to control the mother’s bleeding and drugs to assist the newborn’s
breathing),
and which regularly charges patients for services and supplies, admits only patients with low risk
pregnancies, contracts with an area hospital and displays written procedures for the immediate
transfer of mother and child in emergency cases and has an ongoing quality assurance program
(with reviews by Physicians other than those who own and/or direct the facility).
Certified Registered Nurse Anesthetist (C.R.N.A.) is a Registered Nurse certified to administer
anesthesia, who is employed by and under the personal supervision of a Physician
Anesthesiologist.
Chemical Dependency means Drug Abuse, Substance Abuse or Alcoholism.
Coinsurance means the percentage of charges that the Covered Person is required to pay for
eligible charges/expenses under this Plan.
Confined, when used in connection with a hospital, means a period of twenty-four (24) hour days,
but no less than one such day, during which the Covered Person is confined in a facility for which
there is a daily charge made for room and board.
Continuously Covered means a person has been continuously covered under this Plan.
Copayment or Copay means that amount of Eligible Expense, which the Covered Person is
required to pay before benefits may begin by this Plan.
Cosmetic, Cosmetic Dentistry, Cosmetic Surgery and Cosmetic Procedures means
medically unnecessary surgery or other medical procedures, usually, but not limited to, plastic
surgery which is intended to improve appearance but does not improve function of a body part.
Covered Dependent means an eligible Dependent the Covered Student has elected to include
in this Plan and for whom the Covered Student has submitted any applicable premium required
by this Plan by the due date.
Covered Person means either the Covered Student or the Covered Dependent while coverage
is in force, but in no case can a Covered Person be considered both a Covered Student and a
Covered Dependent under this Plan.
Covered Student means an eligible student who has elected to participate in this Plan and
submitted any applicable premium as required by this Plan by the due date.

6

DEFINITIONS
Custodial Care means any service or supply, including room and board, which is furnished mainly
to help a person meet his or her routine daily needs. Even if the Covered Person is in a hospital
or other recognized facility, this Plan does not pay for care if it is mainly custodial unless
specifically provided for in the schedule of benefits.
Deductible means that amount of Eligible Expense that the Covered Person is required to pay
before benefits are payable under this Plan.
Dentist is a person who is properly trained and licensed to practice dentistry and who is practicing
within the scope of such license.
Dependent means any of the following:
1. The lawful spouse of the Covered Student for whom the Covered Student is legally responsible,
and who is not also a Covered Student, resides with the Covered Student, and is not legally
separated or divorced from the Covered Student.
2. The Covered Student’s same sex or opposite sex domestic partner provided they are living
together and a written declaration of domestic partnership acceptable to this Plan has been
completed and/or any applicable requirements of the state, city and/or country in which they reside
regarding domestic partnership have been met.
3. Any child or stepchild of the Covered Student less than twenty-six (26) years of age.
4. Any unmarried child or stepchild who is at least twenty-six (26) years of age, but under the age of
twenty-seven (27) provided the child is attending an accredited institution of higher learning on a
full-time basis as defined by the school, is living in the same country as the Covered Student (with
the exception of eligible full-time students temporarily studying abroad), and is financially
dependent upon the Covered Student for the major part of support.
5. The Covered Student’s domestic partner’s child under the age of 26, or unmarried age 26 but
under age 27.
6. Any unmarried child or stepchild who is mentally or physically disabled and incapable of earning
a living and entirely dependent upon the Covered Student for support. This Plan will have the right
to require documentation of the disability, but not more often than once every year.
7. Any unmarried child or stepchild of the Covered Student who is at least twenty-six (26) years of
age, but under the age of twenty-seven (27) provided the child or stepchild is not eligible for
coverage under a group health benefit plan that is offered by his or her employer and for which
the amount of his or her premium contribution is no greater than the premium amount for his or
her coverage as a dependent under this Plan.
8. An adult child or stepchild of the Covered Student or Covered Student’s domestic partner
regardless of age if the child was under 27 years of age when he or she was called to federal
active duty in the National Guard or in a reserve component of the U.S. armed forces while the
child was attending, on a full-time basis, an institution of higher education and the child returns to
school as a full-time student within 12 months of fulfilling his or her active duty obligation.

7

DEFINITIONS
Drug Abuse is physical, habitual dependence on drugs. This includes, but is not limited to,
dependence on drugs that are medically prescribed. This does not include tobacco or caffeine
abuse or dependence which Treatment is excluded by this Plan.
Durable Medical/Surgical Equipment and Supplies are:
1. Primarily and customarily used for medical purposes and are not generally useful in the
absence of an Illness or Injury,
2. Can effectively be used in a non-medical facility (home),
3. Are expected to make a significant contribution to the Treatment of an Illness or Injury,
4. Are used solely for the care and Treatment of the patient, and
5. Are priced so that the cost of the equipment/supplies is proportionate to the therapeutic
benefits that can be derived from the use of the equipment/supplies.
Elective Surgical Procedure is a non-emergency surgical procedure, which is scheduled at the
Covered Person’s convenience without endangering the Covered Person’s life or without causing
serious impairment to the Covered Person’s bodily functions.
Eligible Expense means a charge for Treatment not excluded by this Plan resulting from
Treatment of an Accident or Illness that must be:
1. Consistent with the diagnosis and treatment of the Covered Person’s condition,
2. In accordance with standards of good medical practice,
3. Not solely for the convenience of the patient, Physician or supplier,
4. Neither Experimental nor Investigational,
5. Performed in the least costly setting required by the patient’s medical condition. The act of
prescribing a course of Treatment does not automatically mean that Treatment will result in an
Eligible Expense,
6. Within this Plan’s description of Usual, Customary and Reasonable (UCR) expenses,
7. Incurred within a period of time during which the claimant was a Covered Person.
Emergency Services means, with respect to a Medical Emergency:
(a)
a medical screening examination (as required under section 1867 of the Social Security
Act, 42, U.S.C. 1395dd) that is within the capability of the emergency department of a
Hospital, including ancillary services routinely available to the emergency department to
evaluate such Medical Emergency; and
(b)
such further medical examination and treatment, to the extent they are within the
capabilities of the staff and facilities available at the Hospital, as are required under
section 1867 of the Social Security Act (42 U.S.C. 1395dd(e)(3)).
Emergency Services treatment or care rendered by an Out-of-Network provider is mandated by
the Patient Protection and Affordable Care Act to be provided at the same benefit and cost
sharing level as services provided by a Network provider.
Experimental and/or Investigational means services, supplies, care and Treatment which do
not constitute accepted medical practice properly within the range of appropriate medical practice
under the standards of the case and by the standards of a reasonably substantial, qualified,
responsible, relevant segment of the medical community or government oversight agencies at the
time services were rendered.
8
DEFINITIONS
Experimental and/or Investigational (continued)
In determining coverage under this Plan, the Plan Administrator and the Third Party Administrator
shall make an independent evaluation of the experimental status of specific technologies and shall
be guided by a reasonable interpretation of Plan provisions. The decision(s) shall be made in
good faith and will be rendered following a detailed factual background investigation of the claim
and the proposed treatment. In making such a determination, the Plan Administrator and the
Third Party Administrator will be guided by the following principles:
1. If the drug or device cannot be lawfully marketed without approval of the U.S. Food and
Drug Administration and approval for marketing has not been given at the time the drug or
device is furnished; or
2. If the drug, device, medical treatment or procedure, or the patient informed consent document
utilized with the drug, device, treatment or procedure was reviewed and approved by the
treating facility’s Institutional Review Board or other body serving a similar function or if Federal
law requires such review or approval; or
3. If Reliable Evidence shows that the drug, device, medical treatment or procedure is the subject
of ongoing Phase I or Phase II clinical trials, is the research, experimental, study or
investigational arm or ongoing Phase III clinical trials, or is otherwise under study to determine
its maximum tolerated dose, its toxicity, its safety, its efficacy or its efficacy as compared with
a standard means of treatment or diagnosis; or
4. If Reliable Evidence shows that the prevailing opinion among experts regarding the drug,
device, medical treatment or procedure is that further studies or clinical trials are necessary to
determine its maximum tolerated dose, its toxicity, its safety, its efficacy or its efficacy as
compared with a standard means of treatment or diagnosis.
Reliable Evidence shall mean only published reports and articles in the authoritative medical and
scientific literature; the written protocol or protocols used by the treating facility or the protocol(s)
of another facility studying substantially the same drug, device, medical treatment or procedure;
or the written informed consent used by the treating facility or by another facility studying
substantially the same drug, device, medical treatment or procedure.
The decisions of the Plan Administrator and the Third Party Administrator will be final and binding
on this Plan.
Generic Drug means a prescription drug, which has the equivalency of the brand name drug with
the same use and metabolic disintegration. This Plan will consider as a Generic Drug any Food
and Drug Administration approved generic pharmaceutical dispensed according to the
professional standards of a licensed Pharmacist and clearly designated by the Pharmacist as
being generic.
Home Health Care means part-time or intermittent nursing care, including the Medically
Necessary supplies for treatment of the Covered Illness or Injury. Home health care must be in
place of Hospital confinement.

9
DEFINITIONS
Hospice means a facility or program providing a coordinated program of home and inpatient
care which treats terminally ill patients. The program provides care to meet the special needs of
the patient during the final stages of a terminal illness. Care is provided by a team made up of
trained medical personnel, counselors and volunteers. The team acts under an independent
hospice administration and it helps the patient cope with physical, psychological, spiritual, social
and economic stresses. The hospice administration must meet the standards of the National
Hospice Organization and any licensing requirement.
Hospital means an institution which:
1. Maintains permanent and full-time facilities for bed care of resident patients,
2. Has a licensed Physician in regular full-time attendance,
3. Continuously provides 24 hour-a-day nursing service by Registered Nurses,
4. Has on-premises surgical facilities,
5. Is primarily engaged in providing diagnostic, surgical, medical and therapeutic facilities for the
care of injured and sick persons on a basis other than as a rest home, nursing home,
convalescent home, a place for custodial or educational care, a place for the aged, a place for
substance abusers or as an institution mainly rendering treatment or services for mental or
nervous disorders, and
6. Is licensed and operating lawfully in the jurisdiction where it is located.
7. This does not include a Government Facility.
Illness means disease or sickness including related conditions and recurrent symptoms of the
Illness. Illness also includes pregnancy and complications of pregnancy.
Injury means bodily injury caused by an Accident. This includes related conditions and recurrent
symptoms of such injury.
In-Network describes a provider or health care facility which is part of a health plan’s network of
providers. Providers are contracted with the network entity to provide lower health care expenses
to the Plan and the member.
Intensive Care Unit means Hospital special twenty-four (24) hour nursing care and equipment in
a room other than a Ward, Semi-Private, or Private room, which services are made necessary by
the Covered Person’s critical medical condition and which provides other than normal, routine
treatment.
Lifetime is a word that appears in this Plan in reference to benefit maximums and limitations.
Lifetime is understood to mean while covered under this Plan. Under no circumstances does
Lifetime mean during the lifetime of the Covered Person.
Medical Emergency means a sudden onset of acute symptoms of sufficient severity that the
absence of immediate medical attention could result in serious jeopardy to the participant’s health
or bodily functions, or with respect to a pregnancy, could result in serious jeopardy to the health
of the woman or her unborn child. In addition, Medical Emergency includes a mental health or
chemical dependency condition when the lack of medical treatment could reasonably be expected
to result in the Covered Person harming oneself and/or other persons.
10

DEFINITIONS
Medically Necessary means any health care treatment, service or supply determined by the Plan
Administrator to meet each of these requirements:
1. It is ordered by a Physician for the diagnosis or treatment of a covered Illness or Injury;
2. The prevailing opinion within the appropriate specialty of the United States medical profession
is that it is safe and effective for its intended use, and that omission would adversely affect the
person’s medical condition; and
3. It is furnished by a provider with appropriate training, experience, staff and facilities to furnish
that particular service or supply.
The Plan Administrator and the Third Party Administrator will determine whether these
requirements have been met based on: 1) published reports in authoritative medical and scientific
literature; 2) regulations, reports, publications or evaluations issued by government agencies such
as the Agency for Health Care Policy and Research, the National Institute of Health, and the Food
and Drug Administration's (FDA); 3) listings in the following compendia: The American Medication
Association Drug Evaluations, the American Hospital Formulary Service Drug Information and
The United States Pharmacopoeia Dispensing Information; and 4) other authoritative medical
sources to the extent that the Third Party Administrator determines them to be necessary.
Mental Health Conditions means a condition characterized by abnormal functioning of the mind
or emotions and in which psychological, intellectual, emotional or behavioral disturbances are the
dominant feature. Mental Health Conditions include mental disorders, mental Illnesses,
psychiatric Illnesses, mental conditions, behavioral conditions, and psychiatric conditions,
whether organic or non-organic, whether of biological, non-biological, genetic, chemical or nonchemical origin, and irrespective of cause, basis or inducement.
Morbid Obesity is defined as when a person’s body weight exceeds the medically recommended
weight by either one hundred (100) pounds or is twice the medically recommended weight for a
person of the same gender, height, age and mobility.
Newborn Dependent means any child for whom birth occurred while the student was a Covered
Person under this Plan.
Non-Occupational Disease or Injury means an Illness or Injury which does not arise out of, and
which is not caused or contributed by, nor is a consequence of, or in the course of, any
employment or occupation for compensation and profit.
Out-of-Network describes a provider or health care facility which is not part of a health plan’s
network of providers. Members may pay more when using an out-of-network provider since
there is no contracted amount for health care expenses.
Out-of-Pocket Expenses means that portion of Eligible Expenses for which the Covered Person
is responsible as the result of Coinsurance, Copayments and Deductible.

11

DEFINITIONS
Partial Hospitalization refers to services, supplies and Treatment in an approved facility for not
less than four (4) hours or more than sixteen (16) hours in any twenty-four (24) hour period.
Participating Provider or Network Provider is a provider, such as a Physician, Hospital, or
other health facility or provider who is under a contractual agreement with this Plan to provide
care or services to Covered Persons.
Payable Expense is the balance of Eligible Expenses remaining after the application of
deductibles, coinsurance, copayments, discounts and that is submitted to this Plan for payment
within the Timely Filing period.
Physician means a person, other than a member of the Covered Person’s immediate family, a
blood relative, or a person who normally lives in the Covered Person’s home and who
1. Has a designation of either M.D., D.O., D.P.M., or
2. A provider acting within the scope of the license provided by the state in which the Physician
practices.
Plan means this entire document.
Plan Year means the entire Plan Year beginning on August 15th through August 14th.
Preventive Care means routine examinations, physicals, gynecological exam, immunizations,
routine urinalysis and other routine screening tests.
Preventive Services mandated by the Patient Protection and Affordable Care Act and, in
addition to any other preventive benefits described in this Plan, means the following services
and without the imposition of any cost-sharing requirements, such as deductibles, copayment
amounts or coinsurance amounts to any Covered Person receiving any of the following:
1.
Evidence-based items or services that have in effect a rating of “A” or “B” in the current
recommendations of the United States Preventive Services Task Force, except that the
current recommendations of the United States Preventive Service Task Force regarding
breast cancer screening, mammography, and prevention of breast cancer shall be
considered the most current other than those issued in or around November 2009;
2.
Immunizations that have in effect a recommendation from the Advisory Committee on
Immunization Practices of the Centers for Disease Control and Prevention with respect to
the Covered Person involved;
3.
With respect to infants, children, and adolescents, evidence-informed preventive care and
screenings provided for in the comprehensive guidelines supported by the Health
resources and Services Administration; and
4.
With respect to women, such additional preventive care and screenings, not described in
paragraph 1 above, as provided for in comprehensive guidelines supported by the Health
Resources and Services Administration.
This Plan shall update new recommendations to the preventive benefits listed above at the
schedule established by the Secretary of Health and Human Services.
DEFINITIONS
Primary Care is the first care a patient receives for a covered Illness or Injury.
Provider of Services means a Physician or any legally recognized supplier of medical services
or supplies operating at the direction of the Covered Person’s Attending Physician which services
or supplies can be described as Eligible Expenses.
Psychologist means a person, other than a member of the Covered Person’s immediate family,
with a degree of Ph.D. or Ed.D. operating at the direction of the Covered Person’s Attending
Physician which services or supplies can be described as Eligible Expenses.
Registered Nurse means a professional nurse, other than a member of the Covered Person’s
immediate family, enabled to use the title Registered Nurse and its designation R.N., performing
the duties and acting within the scope of the license provided by the state in which practicing.
Rehabilitation Facility, Extended Care Facility, Skilled Nursing Facility, Convalescent Care
Facility, and Residential Center all mean an institution, other than a Hospital, licensed by the
state where located, which exists for the purpose of active rehabilitation of patients during a Period
of Confinement and which
1. Provides skilled nursing care under twenty-four (24) hour a day supervision of an Active, FullTime Physician or Registered Nurse,
2. Has available at all times the services of a Physician who is a Hospital staff member,
3. Maintains a daily record for each patient, and
4. Is not a place, except incidentally, for
a. Rest,
b. Custodial Care,
c. The aged,
d. The care of drug addicts nor alcoholics, and
5. Is not a hotel, domiciliary care neither home, nor similar institution, and
6. Is licensed and operating lawfully in the jurisdiction where it is located.
Second Surgical Opinion means another opinion on an anticipated surgical procedure which
opinion is rendered by a Surgeon who is not:
1. The Physician who originally recommended the surgery;
2. A partner in practice with the Physician who originally recommended the surgery;
3. The Physician who actually performs the procedure in question.
Semi-Private means a two-bed room accommodation.
Sound Natural Teeth means natural teeth, the major portion of the individual tooth, which is
present regardless of fillings and is not carious, abscessed, or defective. Sound natural teeth shall
not include capped teeth.
Speech Therapist, Physical Therapist, Occupational Therapist, Respiratory Therapist
means a licensed person or institution providing therapy, or, if licensing is not required, the
therapist is certified by his or her national organization or association.
13
DEFINITIONS
Substance Abuse or Chemical Dependency, see Alcoholism and Drug Abuse.
Surgical Center, see Ambulatory Surgical Center
Temporomandibular Joint Syndrome (TMJ) is the treatment of jaw joint disorders including
conditions of structures linking the jawbone and skull and the complex of muscles, nerves and
other tissues related to the temporomandibular joint.
Treatment means any contact with any provider of health care involving the condition in question
or the taking of any medicine prescribed for the condition in question.
University means University of Wisconsin-Madison
University Health Services means any organization, facility or clinic operated, maintained or
supported by the University or other entity under contract with the University which provides health
care services to Covered Persons.
Urgent Care means care for an unexpected Illness or Injury which does not require use of a
Hospital’s Emergency Room, but which may need prompt attention, and include, but are not
limited to: cold, sore throat, cough, fever, vomiting, sprain or strain, cramps, diarrhea, bumps and
bruises, small lacerations, minor burns, earache, rashes, swollen glands, conjunctivitis.
Usual, Customary and Reasonable (UCR), when used in connection with a fee for Treatment,
means the lesser of
1. the actual charge, or
2. usual & customary charges as determined by FAIR Health, Inc.
but never more than the provider of Treatment accepts from any other source of payment of
charges for the same treatment.
You, Your means the Covered Student.
        """

        answerAgent = Agent(
            role="Query Answering",
            goal="Answer the question the user asks using the definitions provided",
            backstory="You are an AI agent that will answer user questions using the definitions provided. " +
                        "Keep the answer concise and to the point." +
                        "Add a few examples in bullet point format with the context of health insurance to make the answer more understandable." +
                        f"Here are the definitions: {pdf}." +
                        "Do not write any notes or personal remarks like 'here is the definition'.",
            verbose=False,
            allow_delegation=False
        )

        answerTask = Task(
            description=f"answer {content.content}",
            agent=answerAgent,
            expected_output="A definition of the term the user asked about and a few examples",
        )

        answerCrew = Crew(
            agents=[answerAgent],
            tasks=[answerTask],
            verbose=0,
            process=Process.sequential
        )
 
        # Execute the crews and get the results
        answer = answerCrew.kickoff()
 
        # Combine the results into a single response
        result = {
            "Answer": answer
        }
 
        return result
 
if __name__ == "__main__":
    uvicorn.run("ship:app", host="127.0.0.1", port=8001, reload=True)