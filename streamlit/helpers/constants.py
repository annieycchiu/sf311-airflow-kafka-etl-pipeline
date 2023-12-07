# set up available police districts for the dahsboard drop down list
police_district_list = [
    'All', 'Bayview', 'Central', 'Ingleside', 'Mission', 'Northern', 
    'Park', 'Richmond', 'Southern', 'Taraval', 'Tenderloin']

# set up available service types for the dashboard drop down list
service_types_list = [
    'All', 'Abandoned Vehicle', 'Damaged Property', 'Encampments', 'General Request - MTA',
    'General Request - PUBLIC WORKS', 'Graffiti', 'Illegal Postings', 'Litter Receptacles',
    'Muni Employee Feedback', 'Muni Service Feedback', 'Noise Report', 'Parking Enforcement',
    'Rec and Park Requests', 'Sewer Issues', 'Sidewalk or Curb', 'Sign Repair',
    'Street Defects', 'Street and Sidewalk Cleaning', 'Streetlights', 'Tree Maintenance']

# set up mapping table of service types for FastAPI input data format
service_mapping = {
    'Abandoned Vehicle': 0,
    'Damaged Property': 1,
    'Encampments': 2,
    'General Request - MTA': 3,
    'General Request - PUBLIC WORKS': 4,
    'Graffiti': 5,
    'Illegal Postings': 6,
    'Litter Receptacles': 7,
    'Muni Employee Feedback': 8,
    'Muni Service Feedback': 9,
    'Noise Report': 10,
    'Others': 11,
    'Parking Enforcement': 12,
    'Rec and Park Requests': 13,
    'Sewer Issues': 14,
    'Sidewalk or Curb': 15,
    'Sign Repair': 16,
    'Street Defects': 17,
    'Street and Sidewalk Cleaning': 18,
    'Streetlights': 19,
    'Tree Maintenance': 20}

# set up mapping table of police districts for FastAPI input data format
police_mapping = {
    'Bayview': 21,
    'Central': 22,
    'Ingleside': 23,
    'Mission': 24,
    'Northern': 25,
    'Park': 26,
    'Richmond': 27,
    'Southern': 28,
    'Taraval': 29,
    'Tenderloin': 30}