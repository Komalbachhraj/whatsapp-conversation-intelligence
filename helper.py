# from urlextract import URLExtract
# from wordcloud import WordCloud
# import pandas as pd
# from collections import Counter
# import emoji
# import os
#
# extract = URLExtract()
#
# def fetch_stats(selected_user,df):
#
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#
#     # fetch the number of messages
#     num_messages = df.shape[0]
#
#     # fetch the total number of words
#     words = []
#     for message in df['message']:
#         words.extend(message.split())
#
#     # fetch number of media messages
#     num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
#
#     # fetch number of links shared
#     links = []
#     for message in df['message']:
#         links.extend(extract.find_urls(message))
#
#     return num_messages,len(words),num_media_messages,len(links)
#
# def most_busy_users(df):
#     x = df['user'].value_counts().head()
#     df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
#         columns={'index': 'name', 'user': 'percent'})
#     return x,df
#
# def create_wordcloud(selected_user, df):
#
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#     stopwords_path = os.path.join(BASE_DIR, "stop_hinglish.txt")
#
#     # Read stop words
#     with open(stopwords_path, "r", encoding="utf-8") as f:
#         stop_words = set(f.read().splitlines())
#
#     # Select user
#     if selected_user != 'Overall':
#         temp = df[df['user'] == selected_user].copy()
#     else:
#         temp = df.copy()
#
#     # Remove group notifications
#     temp = temp[temp['user'] != 'group_notification'].copy()
#
#     # Remove media messages
#     temp = temp[temp['message'] != '<Media omitted>\n'].copy()
#
#     # Handle NaN values and make everything a string
#     temp['message'] = temp['message'].fillna('').astype(str)
#
#     # Remove stop words
#     def remove_stop_words(message):
#         words = []
#
#         for word in message.lower().split():
#             if word not in stop_words:
#                 words.append(word)
#
#         return " ".join(words)
#
#     temp['message'] = temp['message'].apply(remove_stop_words)
#
#     # Combine all messages
#     text = temp['message'].str.cat(sep=" ")
#
#     # No text available
#     if not text.strip():
#         return None
#
#     # Generate WordCloud
#     wc = WordCloud(
#         width=500,
#         height=500,
#         min_font_size=10,
#         background_color='white'
#     )
#
#     df_wc = wc.generate(text)
#
#     return df_wc
#
# # def create_wordcloud(selected_user,df):
# #     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# #     stopwords_path = os.path.join(BASE_DIR, "stop_hinglish.txt")
# #
# #     with open(stopwords_path, "r", encoding="utf-8") as f:
# #         stop_words = f.read().splitlines()
# #
# #     if selected_user != 'Overall':
# #         df = df[df['user'] == selected_user]
# #
# #     temp = df[df['user'] != 'group_notification']
# #     temp = temp[temp['message'] != '<Media omitted>\n']
# #
# #     def remove_stop_words(message):
# #         y = []
# #         for word in message.lower().split():
# #             if word not in stop_words:
# #                 y.append(word)
# #         return " ".join(y)
# #
# #     wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
# #     temp['message'] = temp['message'].apply(remove_stop_words)
# #     df_wc = wc.generate(temp['message'].str.cat(sep=" "))
# #     return df_wc
#
# def most_common_words(selected_user,df):
#
#     f = open('stop_hinglish.txt','r')
#     stop_words = f.read()
#
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#
#     temp = df[df['user'] != 'group_notification']
#     temp = temp[temp['message'] != '<Media omitted>\n']
#
#     words = []
#
#     for message in temp['message']:
#         for word in message.lower().split():
#             if word not in stop_words:
#                 words.append(word)
#
#     most_common_df = pd.DataFrame(Counter(words).most_common(20))
#     return most_common_df
#
# def emoji_helper(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#
#     emojis = []
#     for message in df['message']:
#         emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
#
#     emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
#
#     return emoji_df
#
# def monthly_timeline(selected_user,df):
#
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#
#     timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
#
#     time = []
#     for i in range(timeline.shape[0]):
#         time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
#
#     timeline['time'] = time
#
#     return timeline
#
# def daily_timeline(selected_user,df):
#
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#
#     daily_timeline = df.groupby('only_date').count()['message'].reset_index()
#
#     return daily_timeline
#
# def week_activity_map(selected_user,df):
#
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#
#     return df['day_name'].value_counts()
#
# def month_activity_map(selected_user,df):
#
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#
#     return df['month'].value_counts()
#
# def activity_heatmap(selected_user,df):
#
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#
#     user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
#
#     return user_heatmap


from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import os
import re
import numpy as np

# =========================================================
# ML IMPORTS
# =========================================================

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor


extract = URLExtract()


# =========================================================
# BASIC STATISTICS
# =========================================================

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []

    for message in df['message']:

        message = str(message)

        words.extend(
            message.split()
        )

    # fetch number of media messages

    num_media_messages = df[
        df['message'].astype(str).str.strip().str.lower()
        .isin([
            '<media omitted>',
            'media omitted'
        ])
    ].shape[0]

    # fetch number of links shared

    links = []

    for message in df['message']:

        message = str(message)

        links.extend(
            extract.find_urls(message)
        )

    return (
        num_messages,
        len(words),
        num_media_messages,
        len(links)
    )


# =========================================================
# MOST BUSY USERS
# =========================================================

def most_busy_users(df):

    x = df['user'].value_counts().head()

    df = round(
        (
            df['user'].value_counts()
            / df.shape[0]
        ) * 100,
        2
    ).reset_index().rename(
        columns={
            'index': 'name',
            'user': 'percent'
        }
    )

    return x, df


# =========================================================
# WORDCLOUD
# =========================================================

def create_wordcloud(selected_user, df):

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    stopwords_path = os.path.join(
        BASE_DIR,
        "stop_hinglish.txt"
    )

    # Read stop words
    with open(
        stopwords_path,
        "r",
        encoding="utf-8"
    ) as f:

        stop_words = set(
            f.read().splitlines()
        )

    # Select user
    if selected_user != 'Overall':

        temp = df[
            df['user'] == selected_user
        ].copy()

    else:

        temp = df.copy()

    # Remove group notifications
    temp = temp[
        temp['user'] != 'group_notification'
    ].copy()

    # Remove media messages
    temp = temp[
        ~temp['message']
        .astype(str)
        .str.strip()
        .str.lower()
        .isin([
            '<media omitted>',
            'media omitted'
        ])
    ].copy()

    # Handle NaN values
    temp['message'] = (
        temp['message']
        .fillna('')
        .astype(str)
    )

    # Remove stop words
    def remove_stop_words(message):

        words = []

        for word in message.lower().split():

            if word not in stop_words:

                words.append(word)

        return " ".join(words)

    temp['message'] = (
        temp['message']
        .apply(remove_stop_words)
    )

    # Combine all messages
    text = temp['message'].str.cat(
        sep=" "
    )

    # No text available
    if not text.strip():

        return None

    # Generate WordCloud
    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color='white'
    )

    df_wc = wc.generate(text)

    return df_wc


# =========================================================
# MOST COMMON WORDS
# =========================================================

def most_common_words(selected_user, df):

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    stopwords_path = os.path.join(
        BASE_DIR,
        "stop_hinglish.txt"
    )

    # Read stop words
    with open(
        stopwords_path,
        "r",
        encoding="utf-8"
    ) as f:

        stop_words = set(
            word.strip().lower()
            for word in f.read().splitlines()
            if word.strip()
        )

    # Select user
    if selected_user != 'Overall':

        df = df[
            df['user'] == selected_user
        ]

    # Remove group notifications
    temp = df[
        df['user'] != 'group_notification'
    ].copy()

    # Handle missing messages
    temp['message'] = (
        temp['message']
        .fillna('')
        .astype(str)
    )

    # Remove media messages
    temp = temp[
        ~temp['message']
        .str.strip()
        .str.lower()
        .isin([
            '<media omitted>',
            '<media omitted>\n',
            'media omitted'
        ])
    ]

    # Remove deleted-message notifications
    temp = temp[
        ~temp['message']
        .str.lower()
        .str.contains(
            'this message was deleted',
            na=False
        )
    ]

    words = []

    for message in temp['message']:

        message = message.lower()

        # -------------------------------------------------
        # Remove URLs
        # -------------------------------------------------

        message = re.sub(
            r'https?://\S+|www\.\S+',
            ' ',
            message
        )

        # -------------------------------------------------
        # Remove HTML tags
        # -------------------------------------------------

        message = re.sub(
            r'<[^>]*>',
            ' ',
            message
        )

        # -------------------------------------------------
        # Remove CSS-like fragments
        # -------------------------------------------------

        message = re.sub(
            r'\b\d+px\b',
            ' ',
            message
        )

        message = re.sub(
            r'\b(?:padding|margin|center|width|height|font|style|display|color|background)\s*:',
            ' ',
            message
        )

        # -------------------------------------------------
        # Remove punctuation / symbols
        # -------------------------------------------------

        message = re.sub(
            r'[^\w\s]',
            ' ',
            message
        )

        # -------------------------------------------------
        # Split into words
        # -------------------------------------------------

        for word in message.split():

            # Remove stop words
            if word in stop_words:
                continue

            # Remove very short garbage tokens
            if len(word) <= 1:
                continue

            # Ignore pure numbers
            if word.isdigit():
                continue

            words.append(word)

    # -----------------------------------------------------
    # Find 20 most common words
    # -----------------------------------------------------

    most_common = Counter(
        words
    ).most_common(20)

    most_common_df = pd.DataFrame(
        most_common,
        columns=[
            'word',
            'count'
        ]
    )

    return most_common_df


# =========================================================
# EMOJI ANALYSIS
# =========================================================

def emoji_helper(selected_user, df):

    if selected_user != 'Overall':

        df = df[
            df['user'] == selected_user
        ]

    emojis = []

    for message in df['message']:

        message = str(message)

        emojis.extend([
            char
            for char in message
            if char in emoji.EMOJI_DATA
        ])

    emoji_df = pd.DataFrame(
        Counter(emojis).most_common(
            len(Counter(emojis))
        ),
        columns=[
            'emoji',
            'count'
        ]
    )

    return emoji_df


# =========================================================
# MONTHLY TIMELINE
# =========================================================

def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':

        df = df[
            df['user'] == selected_user
        ]

    timeline = df.groupby(
        [
            'year',
            'month_num',
            'month'
        ]
    ).count()['message'].reset_index()

    time = []

    for i in range(
        timeline.shape[0]
    ):

        time.append(
            timeline['month'].iloc[i]
            + "-"
            + str(
                timeline['year'].iloc[i]
            )
        )

    timeline['time'] = time

    return timeline


# =========================================================
# DAILY TIMELINE
# =========================================================

def daily_timeline(selected_user, df):

    if selected_user != 'Overall':

        df = df[
            df['user'] == selected_user
        ]

    daily_timeline = df.groupby(
        'only_date'
    ).count()['message'].reset_index()

    return daily_timeline


# =========================================================
# WEEK ACTIVITY
# =========================================================

def week_activity_map(selected_user, df):

    if selected_user != 'Overall':

        df = df[
            df['user'] == selected_user
        ]

    return df[
        'day_name'
    ].value_counts()


# =========================================================
# MONTH ACTIVITY
# =========================================================

def month_activity_map(selected_user, df):

    if selected_user != 'Overall':

        df = df[
            df['user'] == selected_user
        ]

    return df[
        'month'
    ].value_counts()


# =========================================================
# ACTIVITY HEATMAP
# =========================================================

def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':

        df = df[
            df['user'] == selected_user
        ]

    user_heatmap = df.pivot_table(
        index='day_name',
        columns='period',
        values='message',
        aggfunc='count'
    ).fillna(0)

    return user_heatmap


# =========================================================
# =========================================================
#              REPLY PREDICTION MODULE
# =========================================================
# =========================================================


# =========================================================
# CREATE REPLY DATASET
# =========================================================

def create_reply_dataset(
    df,
    response_window=60
):

    temp = df.copy()

    # -----------------------------------------------------
    # Remove WhatsApp system messages
    # -----------------------------------------------------

    temp = temp[
        temp['user'] != 'group_notification'
    ].copy()

    # -----------------------------------------------------
    # Clean messages
    # -----------------------------------------------------

    temp['message'] = (
        temp['message']
        .fillna('')
        .astype(str)
        .str.strip()
    )

    # -----------------------------------------------------
    # Remove empty messages
    # -----------------------------------------------------

    temp = temp[
        temp['message'] != ''
    ].copy()

    # -----------------------------------------------------
    # Remove media-only messages
    # -----------------------------------------------------

    temp = temp[
        ~temp['message']
        .str.lower()
        .isin([
            '<media omitted>',
            'media omitted'
        ])
    ].copy()

    # -----------------------------------------------------
    # Sort chronologically
    # -----------------------------------------------------

    temp = temp.sort_values(
        'date'
    ).reset_index(
        drop=True
    )

    if temp.empty:

        return pd.DataFrame()

    # =====================================================
    # GROUP CONSECUTIVE MESSAGES FROM SAME USER
    # =====================================================

    turns = []

    i = 0

    while i < len(temp):

        current_user = temp.loc[
            i,
            'user'
        ]

        messages = [
            temp.loc[
                i,
                'message'
            ]
        ]

        start_time = temp.loc[
            i,
            'date'
        ]

        end_time = temp.loc[
            i,
            'date'
        ]

        j = i + 1

        while (
            j < len(temp)
            and temp.loc[
                j,
                'user'
            ] == current_user
        ):

            messages.append(
                temp.loc[
                    j,
                    'message'
                ]
            )

            end_time = temp.loc[
                j,
                'date'
            ]

            j += 1

        turns.append({

            'sender':
                current_user,

            'message':
                ' '.join(messages),

            'date':
                start_time,

            'end_date':
                end_time

        })

        i = j

    turns_df = pd.DataFrame(
        turns
    )

    if turns_df.empty:

        return pd.DataFrame()

    # =====================================================
    # FIND FIRST RESPONSE
    # =====================================================

    records = []

    for i in range(
        len(turns_df)
    ):

        sender = turns_df.loc[
            i,
            'sender'
        ]

        message = turns_df.loc[
            i,
            'message'
        ]

        message_time = turns_df.loc[
            i,
            'end_date'
        ]

        first_responder = None

        response_time = None

        # -------------------------------------------------
        # Look for next message from another user
        # -------------------------------------------------

        for j in range(
            i + 1,
            len(turns_df)
        ):

            next_sender = turns_df.loc[
                j,
                'sender'
            ]

            next_time = turns_df.loc[
                j,
                'date'
            ]

            difference = (
                next_time
                - message_time
            ).total_seconds() / 60

            # If response takes more than
            # response_window minutes,
            # treat it as no reply.
            if difference > response_window:

                break

            # Ignore same sender
            if next_sender == sender:

                continue

            # Different sender = reply
            first_responder = next_sender

            response_time = difference

            break

        # =================================================
        # MESSAGE FEATURES
        # =================================================

        word_count = len(
            message.split()
        )

        message_length = len(
            message
        )

        question_count = message.count(
            '?'
        )

        exclamation_count = message.count(
            '!'
        )

        emoji_count = sum(
            1
            for char in message
            if char in emoji.EMOJI_DATA
        )

        records.append({

            'sender':
                sender,

            'message':
                message,

            'hour':
                message_time.hour,

            'day_of_week':
                message_time.dayofweek,

            'message_length':
                message_length,

            'word_count':
                word_count,

            'question_count':
                question_count,

            'exclamation_count':
                exclamation_count,

            'emoji_count':
                emoji_count,

            'first_responder':
                first_responder,

            'response_time':
                response_time,

            'got_reply':
                1
                if first_responder
                else 0

        })

    reply_df = pd.DataFrame(
        records
    )

    return reply_df


# =========================================================
# TRAIN REPLY MODELS
# =========================================================

def train_reply_models(reply_df):

    if reply_df is None:

        return None

    if reply_df.empty:

        return None

    if len(reply_df) < 30:

        return None

    # =====================================================
    # TF-IDF
    # =====================================================

    vectorizer = TfidfVectorizer(
        max_features=1000,
        ngram_range=(1, 2),
        min_df=1
    )

    X_text = vectorizer.fit_transform(
        reply_df['message']
    )

    # =====================================================
    # NUMERICAL FEATURES
    # =====================================================

    numeric_columns = [

        'hour',

        'day_of_week',

        'message_length',

        'word_count',

        'question_count',

        'exclamation_count',

        'emoji_count'

    ]

    X_numeric = reply_df[
        numeric_columns
    ].values

    # =====================================================
    # COMBINE TF-IDF + NUMERICAL FEATURES
    # =====================================================

    X = np.hstack([

        X_text.toarray(),

        X_numeric

    ])

    # =====================================================
    # MODEL 1
    # WILL MESSAGE GET A REPLY?
    # =====================================================

    y_reply = reply_df[
        'got_reply'
    ]

    reply_model = None

    # Need at least 2 classes
    if y_reply.nunique() >= 2:

        reply_model = RandomForestClassifier(

            n_estimators=150,

            random_state=42,

            class_weight='balanced'

        )

        reply_model.fit(
            X,
            y_reply
        )

    # =====================================================
    # MODEL 2
    # WHO WILL REPLY?
    # =====================================================

    replied_df = reply_df[
        reply_df['got_reply'] == 1
    ].copy()

    responder_model = None

    if (
        len(replied_df) >= 10
        and
        replied_df[
            'first_responder'
        ].nunique() >= 2
    ):

        X_resp_text = vectorizer.transform(
            replied_df['message']
        )

        X_resp_numeric = replied_df[
            numeric_columns
        ].values

        X_resp = np.hstack([

            X_resp_text.toarray(),

            X_resp_numeric

        ])

        y_resp = replied_df[
            'first_responder'
        ]

        responder_model = RandomForestClassifier(

            n_estimators=150,

            random_state=42,

            class_weight='balanced'

        )

        responder_model.fit(

            X_resp,

            y_resp

        )

    # =====================================================
    # MODEL 3
    # RESPONSE TIME
    # =====================================================

    time_model = None

    if len(replied_df) >= 10:

        # Remove invalid response times
        time_training_df = replied_df[
            replied_df[
                'response_time'
            ].notna()
        ].copy()

        if len(time_training_df) >= 10:

            X_time_text = vectorizer.transform(

                time_training_df[
                    'message'
                ]

            )

            X_time_numeric = (
                time_training_df[
                    numeric_columns
                ].values
            )

            X_time = np.hstack([

                X_time_text.toarray(),

                X_time_numeric

            ])

            y_time = time_training_df[
                'response_time'
            ]

            time_model = RandomForestRegressor(

                n_estimators=150,

                random_state=42

            )

            time_model.fit(

                X_time,

                y_time

            )

    # =====================================================
    # RETURN ALL MODELS
    # =====================================================

    return {

        'vectorizer':
            vectorizer,

        'reply_model':
            reply_model,

        'responder_model':
            responder_model,

        'time_model':
            time_model,

        'numeric_columns':
            numeric_columns

    }


# =========================================================
# PREDICT REPLY
# =========================================================

def predict_reply(
    message,
    sender,
    models,
    hour,
    day_of_week
):

    if models is None:

        return None

    message = str(
        message
    ).strip()

    if not message:

        return None

    vectorizer = models[
        'vectorizer'
    ]

    numeric_columns = models[
        'numeric_columns'
    ]

    # =====================================================
    # MESSAGE FEATURES
    # =====================================================

    word_count = len(
        message.split()
    )

    message_length = len(
        message
    )

    question_count = message.count(
        '?'
    )

    exclamation_count = message.count(
        '!'
    )

    emoji_count = sum(

        1

        for char in message

        if char in emoji.EMOJI_DATA

    )

    # =====================================================
    # NUMERICAL FEATURES
    # =====================================================

    numeric_features = np.array([

        [

            hour,

            day_of_week,

            message_length,

            word_count,

            question_count,

            exclamation_count,

            emoji_count

        ]

    ])

    # =====================================================
    # TF-IDF FEATURES
    # =====================================================

    text_features = vectorizer.transform(

        [message]

    )

    # =====================================================
    # COMBINE FEATURES
    # =====================================================

    X = np.hstack([

        text_features.toarray(),

        numeric_features

    ])

    # =====================================================
    # RESULT VARIABLES
    # =====================================================

    reply_probability = 0

    responder_probabilities = {}

    predicted_time = None

    # =====================================================
    # MODEL 1
    # WILL MESSAGE GET REPLY?
    # =====================================================

    reply_model = models[
        'reply_model'
    ]

    if reply_model is not None:

        probabilities = (
            reply_model.predict_proba(X)[0]
        )

        classes = list(
            reply_model.classes_
        )

        if 1 in classes:

            reply_probability = (

                probabilities[
                    classes.index(1)
                ]

                * 100

            )

        else:

            reply_probability = 0

    # =====================================================
    # MODEL 2
    # WHO WILL REPLY?
    # =====================================================

    responder_model = models[
        'responder_model'
    ]

    if responder_model is not None:

        probs = responder_model.predict_proba(
            X
        )[0]

        for user, probability in zip(

            responder_model.classes_,

            probs

        ):

            responder_probabilities[
                user
            ] = probability * 100

    # =====================================================
    # MODEL 3
    # RESPONSE TIME
    # =====================================================

    time_model = models[
        'time_model'
    ]

    if time_model is not None:

        predicted_time = float(

            time_model.predict(X)[0]

        )

        # Response time cannot be negative
        predicted_time = max(
            predicted_time,
            0
        )

    # =====================================================
    # FINAL RESULT
    # =====================================================

    return {

        'reply_probability':
            round(
                reply_probability,
                2
            ),

        'responder_probabilities':
            responder_probabilities,

        'predicted_time':
            predicted_time

    }