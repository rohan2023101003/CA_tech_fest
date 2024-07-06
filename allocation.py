import pandas as pd
import re

def clean_column_names(df):
    df.columns = df.columns.str.lower().str.replace(' ', '')
    return df

def split_group_by_gender(group_df):
    new_groups = []
    for _, group in group_df.iterrows():
        group_id = group['groupid']
        members = group['members']
        gender = group['gender'].lower()

        boys_count, girls_count = 0, 0

        boys_match = re.search(r'(\d+)\s*boys', gender)
        girls_match = re.search(r'(\d+)\s*girls', gender)

        if boys_match:
            boys_count = int(boys_match.group(1))
        if girls_match:
            girls_count = int(girls_match.group(1))

        if boys_count + girls_count == 0:
            if 'boys' in gender:
                boys_count = members
            elif 'girls' in gender:
                girls_count = members

        if boys_count > 0:
            new_groups.append({'groupid': group_id, 'members': boys_count, 'gender': 'boys'})
        if girls_count > 0:
            new_groups.append({'groupid': group_id, 'members': girls_count, 'gender': 'girls'})

    return pd.DataFrame(new_groups)

def allocate_rooms(group_file_path, hostel_file_path):
    group_df = pd.read_csv(group_file_path)
    hostel_df = pd.read_csv(hostel_file_path)
    
    # Clean column names
    group_df = clean_column_names(group_df)
    hostel_df = clean_column_names(hostel_df)

    allocation_result = []

    # Split groups by gender if needed
    group_df = split_group_by_gender(group_df)

    def allocate_group(group_id, members, gender, gender_specific_rooms):
        while members > 0 and not gender_specific_rooms.empty:
            # Try to find a room with an exact capacity match
            exact_room = gender_specific_rooms[gender_specific_rooms['capacity'] == members]
            if not exact_room.empty:
                room = exact_room.iloc[0]
                allocation_result.append({
                    'group_id': group_id,
                    'hostel_name': room['hostelname'],
                    'room_number': room['roomnumber'],
                    'members_allocated': members
                })
                gender_specific_rooms.drop(index=room.name, inplace=True)
                members = 0
            else:
                # Try to find the smallest room that can fit the remaining group members
                suitable_rooms = gender_specific_rooms[gender_specific_rooms['capacity'] > members]
                if not suitable_rooms.empty:
                    room = suitable_rooms.iloc[0]
                    allocation_result.append({
                        'group_id': group_id,
                        'hostel_name': room['hostelname'],
                        'room_number': room['roomnumber'],
                        'members_allocated': members
                    })
                    gender_specific_rooms.at[suitable_rooms.index[0], 'capacity'] -= members
                    if gender_specific_rooms.at[suitable_rooms.index[0], 'capacity'] == 0:
                        gender_specific_rooms.drop(index=room.name, inplace=True)
                    members = 0
                else:
                    # Allocate as many members as possible to the largest available room
                    room = gender_specific_rooms.iloc[0]
                    allocation_result.append({
                        'group_id': group_id,
                        'hostel_name': room['hostelname'],
                        'room_number': room['roomnumber'],
                        'members_allocated': room['capacity']
                    })
                    members -= room['capacity']
                    gender_specific_rooms.drop(index=room.name, inplace=True)

        if members > 0:
            allocation_result.append({
                'group_id': group_id,
                'hostel_name': 'Unallocated',
                'room_number': 'NA',
                'members_allocated': members
            })

    def process_groups(gender_specific_rooms, gender):
        remaining_groups = group_df[group_df['gender'] == gender].copy()
        for _, group in remaining_groups.iterrows():
            group_id = group['groupid']
            members = group['members']
            allocate_group(group_id, members, gender, gender_specific_rooms)

    boys_rooms = hostel_df[hostel_df['gender'].str.lower() == 'boys'].copy()
    girls_rooms = hostel_df[hostel_df['gender'].str.lower() == 'girls'].copy()

    process_groups(boys_rooms, 'boys')
    process_groups(girls_rooms, 'girls')

    result_df = pd.DataFrame(allocation_result)
    result_df.to_csv('uploads/allocation_result.csv', index=False)

    return allocation_result

# Example usage:
# allocation_result = allocate_rooms('group_file.csv', 'hostel_file.csv')
# print(allocation_result)
