from django.db import models
from django.contrib.auth.models import User
from PATIENT.models import Patient
from jsignature.fields import JSignatureField
from jsignature.mixins import JSignatureFieldsMixin

# Create your models here.
class Question(models.Model):
    question=models.TextField()
    username = models.OneToOneField(User,on_delete = models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.question



class Appetite(models.Model):
    heading=models.CharField(max_length=500)
    question=models.TextField()

    def __str__(self):
        return self.heading



class QAnswar(models.Model):
    qno=models.IntegerField()
    questions=models.CharField(max_length=500)
    answars=models.TextField(blank=True,null=True)
    userid = models.ForeignKey(User,on_delete = models.CASCADE, null=True, blank=True)




class Answars(models.Model):
    answars=models.TextField(blank=True,null=True)


class NewCase(models.Model):

    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)

class Category(models.Model):

    category = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.category
    
class Question1(models.Model):

    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    question = models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return self.question
    

class Answer(models.Model):

    question = models.ForeignKey(Question1,on_delete=models.CASCADE,null=True,blank=True)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)    
    last_diagnose = models.CharField(max_length=200,null=True,blank=True)
    duration = models.CharField(max_length=200,null=True,blank=True)
    date = models.DateField(auto_now=True,null=True,blank=True)
    flag = models.BooleanField(default=False)

    def __str__(self):
        return self.last_diagnose

class JSModel(JSignatureFieldsMixin):

    question = models.ForeignKey(Question1,on_delete=models.CASCADE,null=True,blank=True)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)

class PersonalHabitNew(models.Model):

    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)
    desire = models.CharField(max_length=50,null=True,blank=True)
    aversion = models.CharField(max_length=50,null=True,blank=True)
    appetite = models.CharField(max_length=50,null=True,blank=True)
    thirst = models.CharField(max_length=50,null=True,blank=True)
    stool = models.CharField(max_length=50,null=True,blank=True)
    urine = models.CharField(max_length=50,null=True,blank=True)
    sleep = models.CharField(max_length=50,null=True,blank=True)
    dreams = models.CharField(max_length=50,null=True,blank=True)
    date = models.DateField(auto_now=True,null=True,blank=True)

class PersonalHabit(models.Model):

    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)
    weather_hot = models.CharField(max_length=50,null=True,blank=True)
    weather_cold = models.CharField(max_length=50,null=True,blank=True)
    weather_rainy = models.CharField(max_length=50,null=True,blank=True)
    weather_humid = models.CharField(max_length=50,null=True,blank=True)
    weather_dry = models.CharField(max_length=50,null=True,blank=True)
    getting_wet = models.CharField(max_length=50,null=True,blank=True)
    weather_open_air = models.CharField(max_length=50,null=True,blank=True)
    weather_wind = models.CharField(max_length=50,null=True,blank=True)
    weather_seashore = models.CharField(max_length=50,null=True,blank=True)
    weather_noise = models.CharField(max_length=50,null=True,blank=True)
    weather_light = models.CharField(max_length=50,null=True,blank=True)
    weather_strong_smell = models.CharField(max_length=50,null=True,blank=True)
    weather_dust = models.CharField(max_length=50,null=True,blank=True)
    weather_smoke = models.CharField(max_length=50,null=True,blank=True)
    weather_before = models.CharField(max_length=50,null=True,blank=True)
    weather_during = models.CharField(max_length=50,null=True,blank=True)
    weather_after_period = models.CharField(max_length=50,null=True,blank=True)
    weather_touch = models.CharField(max_length=50,null=True,blank=True)
    weather_massage = models.CharField(max_length=50,null=True,blank=True)
    weather_pressure = models.CharField(max_length=50,null=True,blank=True)
    weather_small_closed_place = models.CharField(max_length=50,null=True,blank=True)
    weather_crowds = models.CharField(max_length=50,null=True,blank=True)
    weather_tight_clothes = models.CharField(max_length=50,null=True,blank=True)
    weather_exams = models.CharField(max_length=50,null=True,blank=True)
    weather_interview = models.CharField(max_length=50,null=True,blank=True)
    weather_appointment = models.CharField(max_length=50,null=True,blank=True)
    weather_exercise = models.CharField(max_length=50,null=True,blank=True)
    weather_exertion = models.CharField(max_length=50,null=True,blank=True)
    weather_walk = models.CharField(max_length=50,null=True,blank=True)
    weather_running = models.CharField(max_length=50,null=True,blank=True)
    weather_full_moon = models.CharField(max_length=50,null=True,blank=True)
    weather_new_moon = models.CharField(max_length=50,null=True,blank=True)
    weather_sun = models.CharField(max_length=50,null=True,blank=True)
    weather_change = models.CharField(max_length=50,null=True,blank=True)
    date = models.DateField(auto_now=True,null=True,blank=True)


class InFood(models.Model):

    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)
    sweet = models.CharField(max_length=50,null=True,blank=True)
    bitter = models.CharField(max_length=50,null=True,blank=True)
    bread = models.CharField(max_length=50,null=True,blank=True)
    eggs = models.CharField(max_length=50,null=True,blank=True)
    cold_drinks = models.CharField(max_length=50,null=True,blank=True)
    chocolates = models.CharField(max_length=50,null=True,blank=True)
    mud_chalk_paper = models.CharField(max_length=50,null=True,blank=True)
    salt = models.CharField(max_length=50,null=True,blank=True)
    fat = models.CharField(max_length=50,null=True,blank=True)
    butter = models.CharField(max_length=50,null=True,blank=True)
    meat = models.CharField(max_length=50,null=True,blank=True)
    warm_food_drinks = models.CharField(max_length=50,null=True,blank=True)
    fruits = models.CharField(max_length=50,null=True,blank=True)
    pan = models.CharField(max_length=50,null=True,blank=True)
    sour = models.CharField(max_length=50,null=True,blank=True)
    raw_salad = models.CharField(max_length=50,null=True,blank=True)
    snack = models.CharField(max_length=50,null=True,blank=True)
    fish = models.CharField(max_length=50,null=True,blank=True)
    juice = models.CharField(max_length=50,null=True,blank=True)
    ice_cream = models.CharField(max_length=50,null=True,blank=True)
    spicy = models.CharField(max_length=50,null=True,blank=True)
    vegetables = models.CharField(max_length=50,null=True,blank=True)
    cheese = models.CharField(max_length=50,null=True,blank=True)
    onions = models.CharField(max_length=50,null=True,blank=True)
    garlic = models.CharField(max_length=50,null=True,blank=True)
    milk = models.CharField(max_length=50,null=True,blank=True)
    alcohol = models.CharField(max_length=50,null=True,blank=True)
    smoking = models.CharField(max_length=50,null=True,blank=True)
    any_other = models.CharField(max_length=50,null=True,blank=True)
    date = models.DateField(auto_now=True,null=True,blank=True)

class MentalCausative(models.Model):

    patient = models.ForeignKey(Patient,on_delete = models.CASCADE,null=True,blank=True)
    abandonment = models.CharField(max_length=50,null=True,blank=True)
    abusive_husband = models.CharField(max_length=50,null=True,blank=True)
    abusive_parents = models.CharField(max_length=50,null=True,blank=True)
    after_anger = models.CharField(max_length=50,null=True,blank=True)
    anticipation = models.CharField(max_length=50,null=True,blank=True)
    anxiety = models.CharField(max_length=50,null=True,blank=True)
    abused_punishment = models.CharField(max_length=50,null=True,blank=True)
    apprehends = models.CharField(max_length=50,null=True,blank=True)
    bad_tragedies = models.CharField(max_length=50,null=True,blank=True)
    bereavement = models.CharField(max_length=50,null=True,blank=True)
    boredom = models.CharField(max_length=50,null=True,blank=True)
    business = models.CharField(max_length=50,null=True,blank=True)
    blows = models.CharField(max_length=50,null=True,blank=True)
    beatings = models.CharField(max_length=50,null=True,blank=True)
    bad_news = models.CharField(max_length=50,null=True,blank=True)
    bored = models.CharField(max_length=50,null=True,blank=True)
    contradiction = models.CharField(max_length=50,null=True,blank=True)
    criticism = models.CharField(max_length=50,null=True,blank=True)
    deceived_friendship = models.CharField(max_length=50,null=True,blank=True)
    depressing_emotion = models.CharField(max_length=50,null=True,blank=True)
    disagreement = models.CharField(max_length=50,null=True,blank=True)
    discord_chief = models.CharField(max_length=50,null=True,blank=True)
    discord_friends = models.CharField(max_length=50,null=True,blank=True)
    discord_parents_children = models.CharField(max_length=50,null=True,blank=True)
    domination_colonisation = models.CharField(max_length=50,null=True,blank=True)
    domination_parental = models.CharField(max_length=50,null=True,blank=True)
    domination = models.CharField(max_length=50,null=True,blank=True)
    demand_fullfillment = models.CharField(max_length=50,null=True,blank=True)
    embarrassment = models.CharField(max_length=50,null=True,blank=True)
    excitement = models.CharField(max_length=50,null=True,blank=True)
    emotional = models.CharField(max_length=50,null=True,blank=True)
    excitement_business = models.CharField(max_length=50,null=True,blank=True)
    fail_business = models.CharField(max_length=50,null=True,blank=True)
    failure = models.CharField(max_length=50,null=True,blank=True)
    fear = models.CharField(max_length=50,null=True,blank=True)
    feelings_controlled = models.CharField(max_length=50,null=True,blank=True)
    friendship_deceived = models.CharField(max_length=50,null=True,blank=True)
    fright = models.CharField(max_length=50,null=True,blank=True)
    frustration = models.CharField(max_length=50,null=True,blank=True)
    grief_long_drawn = models.CharField(max_length=50,null=True,blank=True)
    grudges = models.CharField(max_length=50,null=True,blank=True)
    guilt_trapped = models.CharField(max_length=50,null=True,blank=True)
    honour_wounded =  models.CharField(max_length=50,null=True,blank=True)
    humiliation = models.CharField(max_length=50,null=True,blank=True)
    humiliation_criticised =models.CharField(max_length=50,null=True,blank=True)
    horrible_stories = models.CharField(max_length=50,null=True,blank=True)
    indulgence = models.CharField(max_length=50,null=True,blank=True)
    insecurity_children = models.CharField(max_length=50,null=True,blank=True)
    isolation = models.CharField(max_length=50,null=True,blank=True)
    introvert = models.CharField(max_length=50,null=True,blank=True)
    irritable = models.CharField(max_length=50,null=True,blank=True)
    jealous_professional = models.CharField(max_length=50,null=True,blank=True)
    joy = models.CharField(max_length=50,null=True,blank=True)
    loss_familiar = models.CharField(max_length=50,null=True,blank=True)
    loss_wealth = models.CharField(max_length=50,null=True,blank=True)
    love_conditional = models.CharField(max_length=50,null=True,blank=True)
    loss_possession = models.CharField(max_length=50,null=True,blank=True)
    love_unhappy = models.CharField(max_length=50,null=True,blank=True)
    mental_exertion = models.CharField(max_length=50,null=True,blank=True)
    maltreatment_child = models.CharField(max_length=50,null=True,blank=True)
    neat_clean = models.CharField(max_length=50,null=True,blank=True)
    negative_pess = models.CharField(max_length=50,null=True,blank=True)
    need_protect = models.CharField(max_length=50,null=True,blank=True)
    overstrain_mental = models.CharField(max_length=50,null=True,blank=True)
    parental_argument = models.CharField(max_length=50,null=True,blank=True)
    parental_control = models.CharField(max_length=50,null=True,blank=True)
    parental_violence = models.CharField(max_length=50,null=True,blank=True)
    parental_fit = models.CharField(max_length=50,null=True,blank=True)
    past_history_dominate = models.CharField(max_length=50,null=True,blank=True)
    perform_pressure = models.CharField(max_length=50,null=True,blank=True)
    pride = models.CharField(max_length=50,null=True,blank=True)
    prolonged_unhappy = models.CharField(max_length=50,null=True,blank=True)
    quarrel = models.CharField(max_length=50,null=True,blank=True)
    rejection = models.CharField(max_length=50,null=True,blank=True)
    reproaches = models.CharField(max_length=50,null=True,blank=True)
    reserved_displeasure = models.CharField(max_length=50,null=True,blank=True)
    rudeness_children = models.CharField(max_length=50,null=True,blank=True)
    restrictions = models.CharField(max_length=50,null=True,blank=True)
    rudeness_others = models.CharField(max_length=50,null=True,blank=True)
    reverse_fortune = models.CharField(max_length=50,null=True,blank=True)
    ridicule = models.CharField(max_length=50,null=True,blank=True)
    scorned = models.CharField(max_length=50,null=True,blank=True)
    seperation = models.CharField(max_length=50,null=True,blank=True)
    shame = models.CharField(max_length=50,null=True,blank=True)
    socio_cultural = models.CharField(max_length=50,null=True,blank=True)
    stress = models.CharField(max_length=50,null=True,blank=True)
    stress_public = models.CharField(max_length=50,null=True,blank=True)
    alcoholic_father = models.CharField(max_length=50,null=True,blank=True)
    witness_violence = models.CharField(max_length=50,null=True,blank=True)
    terror_wars = models.CharField(max_length=50,null=True,blank=True)
    traumetic_childhood = models.CharField(max_length=50,null=True,blank=True)
    ugly = models.CharField(max_length=50,null=True,blank=True)
    unlovable = models.CharField(max_length=50,null=True,blank=True)
    unfullfillment = models.CharField(max_length=50,null=True,blank=True)
    unwanted = models.CharField(max_length=50,null=True,blank=True)
    unpleasant_news = models.CharField(max_length=50,null=True,blank=True)
    unpredicted_mood_father = models.CharField(max_length=50,null=True,blank=True)
    unloved = models.CharField(max_length=50,null=True,blank=True)
    unusual_office = models.CharField(max_length=50,null=True,blank=True)
    worry = models.CharField(max_length=50,null=True,blank=True)
    wounded_sensitivity = models.CharField(max_length=50,null=True,blank=True)
    wounded_honour = models.CharField(max_length=50,null=True,blank=True)
    wounded_pride = models.CharField(max_length=50,null=True,blank=True)
    date = models.DateField(auto_now=True)

class PersonalityCharacter(models.Model):

    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)
    absentminded =  models.CharField(max_length=50,null=True,blank=True)
    active = models.CharField(max_length=50,null=True,blank=True)
    amiable = models.CharField(max_length=50,null=True,blank=True)
    angry = models.CharField(max_length=50,null=True,blank=True)
    benevolence = models.CharField(max_length=50,null=True,blank=True)
    company_like_dislike = models.CharField(max_length=50,null=True,blank=True)
    energetic = models.CharField(max_length=50,null=True,blank=True)
    extrovert = models.CharField(max_length=50,null=True,blank=True)
    forsaken = models.CharField(max_length=50,null=True,blank=True)
    greedy = models.CharField(max_length=50,null=True,blank=True)
    hurried = models.CharField(max_length=50,null=True,blank=True)
    indifferent = models.CharField(max_length=50,null=True,blank=True)
    impatient = models.CharField(max_length=50,null=True,blank=True)
    impetious = models.CharField(max_length=50,null=True,blank=True)
    introvert = models.CharField(max_length=50,null=True,blank=True)
    irritable = models.CharField(max_length=50,null=True,blank=True)
    jealous = models.CharField(max_length=50,null=True,blank=True)
    methodical = models.CharField(max_length=50,null=True,blank=True)
    mild = models.CharField(max_length=50,null=True,blank=True)
    morose = models.CharField(max_length=50,null=True,blank=True)
    neat_clean = models.CharField(max_length=50,null=True,blank=True)
    neg_pess = models.CharField(max_length=50,null=True,blank=True)
    organised = models.CharField(max_length=50,null=True,blank=True)
    positive_opt = models.CharField(max_length=50,null=True,blank=True)
    punctual = models.CharField(max_length=50,null=True,blank=True)
    quarrelsome = models.CharField(max_length=50,null=True,blank=True)
    restless = models.CharField(max_length=50,null=True,blank=True)
    sentimental_weepy = models.CharField(max_length=50,null=True,blank=True)
    slow = models.CharField(max_length=50,null=True,blank=True)
    sluggish = models.CharField(max_length=50,null=True,blank=True)
    sociable = models.CharField(max_length=50,null=True,blank=True)
    stubborn = models.CharField(max_length=50,null=True,blank=True)
    suspicious = models.CharField(max_length=50,null=True,blank=True)
    sympathetic = models.CharField(max_length=50,null=True,blank=True)
    talkative = models.CharField(max_length=50,null=True,blank=True)
    untidy_unclean = models.CharField(max_length=50,null=True,blank=True)
    absentminded_one = models.CharField(max_length=50,null=True,blank=True)
    affectionate = models.CharField(max_length=50,null=True,blank=True) 
    aggressive = models.CharField(max_length=50,null=True,blank=True)
    ambitious = models.CharField(max_length=50,null=True,blank=True)
    amiable_one = models.CharField(max_length=50,null=True,blank=True)
    anxious = models.CharField(max_length=50,null=True,blank=True)
    artistic = models.CharField(max_length=50,null=True,blank=True)
    assertive = models.CharField(max_length=50,null=True,blank=True)
    bossy = models.CharField(max_length=50,null=True,blank=True)
    broods = models.CharField(max_length=50,null=True,blank=True)
    bubbly = models.CharField(max_length=50,null=True,blank=True)
    careful = models.CharField(max_length=50,null=True,blank=True)
    caring = models.CharField(max_length=50,null=True,blank=True)
    cautious = models.CharField(max_length=50,null=True,blank=True)
    changeable = models.CharField(max_length=50,null=True,blank=True)
    compititive = models.CharField(max_length=50,null=True,blank=True)
    lack_confidence = models.CharField(max_length=50,null=True,blank=True)
    confident = models.CharField(max_length=50,null=True,blank=True)
    conscientious = models.CharField(max_length=50,null=True,blank=True)
    conservative = models.CharField(max_length=50,null=True,blank=True)
    considerate = models.CharField(max_length=50,null=True,blank=True)
    conventional = models.CharField(max_length=50,null=True,blank=True)
    creative = models.CharField(max_length=50,null=True,blank=True)
    discontented = models.CharField(max_length=50,null=True,blank=True)
    dutiful = models.CharField(max_length=50,null=True,blank=True)
    easy_going = models.CharField(max_length=50,null=True,blank=True)
    emotional = models.CharField(max_length=50,null=True,blank=True)
    excitable = models.CharField(max_length=50,null=True,blank=True)
    extrovert_one = models.CharField(max_length=50,null=True,blank=True)
    family_oriented = models.CharField(max_length=50,null=True,blank=True)
    fault_finding = models.CharField(max_length=50,null=True,blank=True)
    fearful = models.CharField(max_length=50,null=True,blank=True)
    friendly = models.CharField(max_length=50,null=True,blank=True)
    fun_loving = models.CharField(max_length=50,null=True,blank=True)
    generous = models.CharField(max_length=50,null=True,blank=True)
    hesistant = models.CharField(max_length=50,null=True,blank=True)
    homely = models.CharField(max_length=50,null=True,blank=True)
    honest = models.CharField(max_length=50,null=True,blank=True)
    humourous = models.CharField(max_length=50,null=True,blank=True)
    impatience = models.CharField(max_length=50,null=True,blank=True)
    independent = models.CharField(max_length=50,null=True,blank=True)
    fear_insects = models.CharField(max_length=50,null=True,blank=True)
    intolerant = models.CharField(max_length=50,null=True,blank=True)
    introvert_one = models.CharField(max_length=50,null=True,blank=True)
    irritable_one = models.CharField(max_length=50,null=True,blank=True)
    jealous_one = models.CharField(max_length=50,null=True,blank=True)
    kind = models.CharField(max_length=50,null=True,blank=True)
    loving = models.CharField(max_length=50,null=True,blank=True)
    loyal = models.CharField(max_length=50,null=True,blank=True)
    materialistic = models.CharField(max_length=50,null=True,blank=True)
    messy = models.CharField(max_length=50,null=True,blank=True)
    mild_one = models.CharField(max_length=50,null=True,blank=True)
    moaning = models.CharField(max_length=50,null=True,blank=True)
    moody = models.CharField(max_length=50,null=True,blank=True)
    lack_of_motivation = models.CharField(max_length=50,null=True,blank=True)
    neg_attitude = models.CharField(max_length=50,null=True,blank=True)
    optimistic = models.CharField(max_length=50,null=True,blank=True)
    outgoing = models.CharField(max_length=50,null=True,blank=True)
    passionate = models.CharField(max_length=50,null=True,blank=True)
    perceptive = models.CharField(max_length=50,null=True,blank=True)
    perfectionist = models.CharField(max_length=50,null=True,blank=True)
    pessimistic = models.CharField(max_length=50,null=True,blank=True)
    planner = models.CharField(max_length=50,null=True,blank=True)
    wants_to_please = models.CharField(max_length=50,null=True,blank=True)
    precocious = models.CharField(max_length=50,null=True,blank=True)
    private = models.CharField(max_length=50,null=True,blank=True)
    strong_principled = models.CharField(max_length=50,null=True,blank=True)
    safe_person = models.CharField(max_length=50,null=True,blank=True)
    selfish = models.CharField(max_length=50,null=True,blank=True)
    sensitive = models.CharField(max_length=50,null=True,blank=True)
    sentimental = models.CharField(max_length=50,null=True,blank=True)
    serious = models.CharField(max_length=50,null=True,blank=True)
    sincere = models.CharField(max_length=50,null=True,blank=True)
    shy = models.CharField(max_length=50,null=True,blank=True)
    sociable_one = models.CharField(max_length=50,null=True,blank=True)
    sociable_friendly = models.CharField(max_length=50,null=True,blank=True)
    soft = models.CharField(max_length=50,null=True,blank=True)
    desires_solitude = models.CharField(max_length=50,null=True,blank=True)
    stubborn_one = models.CharField(max_length=50,null=True,blank=True)
    superstitious = models.CharField(max_length=50,null=True,blank=True)
    sympathetic_one = models.CharField(max_length=50,null=True,blank=True)
    avoids_quarrel = models.CharField(max_length=50,null=True,blank=True)
    reliable = models.CharField(max_length=50,null=True,blank=True)
    resentful = models.CharField(max_length=50,null=True,blank=True)
    reserved = models.CharField(max_length=50,null=True,blank=True)
    restless_one = models.CharField(max_length=50,null=True,blank=True)
    risk_avoid = models.CharField(max_length=50,null=True,blank=True)
    romantic = models.CharField(max_length=50,null=True,blank=True)
    follows_routine = models.CharField(max_length=50,null=True,blank=True)
    date = models.DateField(auto_now=True,null=True,blank=True)

class MiasmOne(models.Model):

    patient = models.ForeignKey(Patient,on_delete= models.CASCADE,null = True, blank = True)
    psora = models.CharField(max_length=50,null=True,blank=True)
    sycosis = models.CharField(max_length=50,null=True,blank=True)
    syphilis = models.CharField(max_length=50,null=True,blank=True)
    tubercular = models.CharField(max_length=50,null=True,blank=True)
    psora_sycosis = models.CharField(max_length=50,null=True,blank=True)
    psora_syphilis = models.CharField(max_length=50,null=True,blank=True)
    date = models.DateField(auto_now=True)

class RubricOne(models.Model):

    patient = models.ForeignKey(Patient, on_delete= models.CASCADE, null=True,blank=True)
    rubric = models.CharField(max_length=50 , null=True,blank=True)
    date = models.DateField(auto_now=True)

class Diseases(models.Model):

    name = models.CharField(max_length=150,null=True,blank=True)

    def __str__(self):
        return self.name

class PastHistory(models.Model):

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True,blank=True)
    disease =  models.ForeignKey(Diseases, on_delete=models.CASCADE, null=True,blank=True)
    last_diagnose = models.CharField(max_length=200,null=True,blank=True)
    duration = models.CharField(max_length=200,null=True,blank=True)
    date = models.DateField(auto_now=True,null=True,blank=True)


class Complain(models.Model):

    name = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return self.name
    
class PresentComplaintsNew(models.Model):

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True,blank=True)
    complain = models.ForeignKey(Complain,on_delete=models.CASCADE,null=True,blank=True)
    duration = models.CharField(max_length=50,null=True,blank=True)
    duration_suffix = models.CharField(max_length=100,null=True,blank=True)
    remarks = models.CharField(max_length=250,null=True,blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.complain.name

class PatientHistoryNEW(models.Model):

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True,blank=True)
    complain = models.ForeignKey(Complain,on_delete=models.PROTECT,null=True,blank=True)
    last_diagnosed = models.CharField(max_length=100,null=True,blank=True)
    last_suffix = models.CharField(max_length=50,null=True,blank=True)
    duration = models.CharField(max_length=50,null=True,blank=True)
    duration_suffix = models.CharField(max_length=100,null=True,blank=True)
    remarks = models.CharField(max_length=250,null=True,blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.complain.name



class NewCaseModel(JSignatureFieldsMixin):

    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.patient.case

class FamilyMedicalComplain(models.Model):

    name = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return self.name

class FamilyMedicalHistory(models.Model):

    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)
    relation = models.CharField(max_length=100,null=True,blank=True)
    list_of_disease= models.CharField(max_length=300,null=True,blank=True)
    any_other = models.CharField(max_length=300,null=True,blank=True)
    dead_alive = models.CharField(max_length=10,null=True,blank=True)
    age = models.IntegerField(null=True,blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.patient)
    
class MentalCausativeNewone(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name
    

class MentalCausativeRecord(models.Model):

    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)
    factors = models.CharField(max_length=500,null=True,blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.factors
    
class MentalPersonalityNewOne(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name
    
class MentalPersonalityRecord(models.Model):

    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)
    characters = models.CharField(max_length=500,null=True,blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.characters

class MiasmNewOne(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name
    
class MiasmRecords(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)
    records = models.CharField(max_length=500,null=True,blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.records

class ThermalReactionNewOne(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name
    
class ThermalReactionRecords(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)
    records = models.CharField(max_length=200,null=True,blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.records
    
class MedicineStock(models.Model):
    medicine = models.CharField(max_length=50, blank=True, null=True)
    potency = models.CharField(max_length=50,blank=True,null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    arrival_date = models.DateTimeField(auto_now_add=True, auto_now=False)	
    
    def __str__(self):
        return self.medicine