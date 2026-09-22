# import streamlit as st
# import preprocessor,helper
# import matplotlib.pyplot as plt
# import seaborn as sns
#
# st.sidebar.title("Whatsapp Chat Analyzer")
#
# uploaded_file = st.sidebar.file_uploader("Choose a file")
# if uploaded_file is not None:
#     bytes_data = uploaded_file.getvalue()
#     try:
#         data = bytes_data.decode("utf-8")
#     except UnicodeDecodeError:
#         data = bytes_data.decode("utf-8", errors="replace")
#     df = preprocessor.preprocess(data)
#
#     # fetch unique users
#     user_list = df['user'].unique().tolist()
#     if 'group_notification' in user_list:
#         user_list.remove('group_notification')
#     user_list.sort()
#     user_list.insert(0,"Overall")
#
#     selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
#
#     if st.sidebar.button("Show Analysis"):
#
#         # Stats Area
#         num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
#         st.title("Top Statistics")
#         col1, col2, col3, col4 = st.columns(4)
#
#         with col1:
#             st.header("Total Messages")
#             st.title(num_messages)
#         with col2:
#             st.header("Total Words")
#             st.title(words)
#         with col3:
#             st.header("Media Shared")
#             st.title(num_media_messages)
#         with col4:
#             st.header("Links Shared")
#             st.title(num_links)
#
#         # monthly timeline
#         st.title("Monthly Timeline")
#         timeline = helper.monthly_timeline(selected_user,df)
#         fig,ax = plt.subplots()
#         ax.plot(timeline['time'], timeline['message'],color='green')
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)
#
#         # daily timeline
#         st.title("Daily Timeline")
#         daily_timeline = helper.daily_timeline(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)
#
#         # activity map
#         st.title('Activity Map')
#         col1,col2 = st.columns(2)
#
#         with col1:
#             st.header("Most busy day")
#             busy_day = helper.week_activity_map(selected_user,df)
#             fig,ax = plt.subplots()
#             ax.bar(busy_day.index,busy_day.values,color='purple')
#             plt.xticks(rotation='vertical')
#             st.pyplot(fig)
#
#         with col2:
#             st.header("Most busy month")
#             busy_month = helper.month_activity_map(selected_user, df)
#             fig, ax = plt.subplots()
#             ax.bar(busy_month.index, busy_month.values,color='orange')
#             plt.xticks(rotation='vertical')
#             st.pyplot(fig)
#
#         st.title("Weekly Activity Map")
#         user_heatmap = helper.activity_heatmap(selected_user,df)
#         if user_heatmap.empty:
#             st.warning("Not enough data to generate the heatmap.")
#         else:
#             fig, ax = plt.subplots()
#             ax = sns.heatmap(user_heatmap)
#             st.pyplot(fig)
#
#         # finding the busiest users in the group(Group level)
#         if selected_user == 'Overall':
#             st.title('Most Busy Users')
#             x,new_df = helper.most_busy_users(df)
#             fig, ax = plt.subplots()
#
#             col1, col2 = st.columns(2)
#
#             with col1:
#                 ax.bar(x.index, x.values,color='red')
#                 plt.xticks(rotation='vertical')
#                 st.pyplot(fig)
#             with col2:
#                 st.dataframe(new_df)
#
#         # Wordcloud
#         st.title("Wordcloud")
#
#         try:
#             df_wc = helper.create_wordcloud(selected_user, df)
#
#             if df_wc is not None:
#                 fig, ax = plt.subplots(figsize=(10, 5))
#
#                 ax.imshow(
#                     df_wc.to_array(),
#                     interpolation='bilinear'
#                 )
#
#                 ax.axis('off')
#
#                 st.pyplot(fig)
#                 plt.close(fig)
#
#             else:
#                 st.info("Not enough text data to generate the Wordcloud.")
#
#         except Exception as e:
#             st.warning(f"Wordcloud could not be generated: {e}")
#         # # WordCloud
#         # st.title("Wordcloud")
#         # df_wc = helper.create_wordcloud(selected_user,df)
#         # fig,ax = plt.subplots()
#         # ax.imshow(df_wc)
#         # st.pyplot(fig)
#
#         # most common words
#         most_common_df = helper.most_common_words(selected_user,df)
#
#         fig,ax = plt.subplots()
#
#         ax.barh(most_common_df[0],most_common_df[1])
#         plt.xticks(rotation='vertical')
#
#         st.title('Most commmon words')
#         st.pyplot(fig)
#
#         # emoji analysis
#         emoji_df = helper.emoji_helper(selected_user,df)
#         st.title("Emoji Analysis")
#
#         col1,col2 = st.columns(2)
#
#         with col1:
#             st.dataframe(emoji_df)
#         with col2:
#             fig,ax = plt.subplots()
#             ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
#             st.pyplot(fig)
import streamlit as st
import preprocessor
import helper

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# =========================================================
# PAGE / SIDEBAR
# =========================================================

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader(
    "Choose a file"
)


# =========================================================
# IF FILE IS UPLOADED
# =========================================================

if uploaded_file is not None:

    # =====================================================
    # READ FILE
    # =====================================================

    bytes_data = uploaded_file.getvalue()

    try:

        data = bytes_data.decode(
            "utf-8"
        )

    except UnicodeDecodeError:

        data = bytes_data.decode(
            "utf-8",
            errors="replace"
        )

    # =====================================================
    # PREPROCESS DATA
    # =====================================================

    df = preprocessor.preprocess(
        data
    )

    st.write(
        "Messages detected:",
        df.shape[0]
    )

    st.dataframe(
        df.head()
    )

    # =====================================================
    # FETCH UNIQUE USERS
    # =====================================================

    user_list = (
        df['user']
        .unique()
        .tolist()
    )

    if 'group_notification' in user_list:

        user_list.remove(
            'group_notification'
        )

    user_list.sort()

    user_list.insert(
        0,
        "Overall"
    )

    # =====================================================
    # USER SELECTION
    # =====================================================

    selected_user = st.sidebar.selectbox(

        "Show analysis wrt",

        user_list

    )


    # =====================================================
    # SHOW ANALYSIS BUTTON
    # =====================================================

    show_analysis = st.sidebar.button(
        "Show Analysis"
    )


    # =========================================================
    # NORMAL WHATSAPP CHAT ANALYSIS
    #
    # IMPORTANT:
    # Reply Prediction is NOT inside this block.
    # =========================================================

    if show_analysis:

        # =====================================================
        # STATS AREA
        # =====================================================

        num_messages, words, num_media_messages, num_links = (
            helper.fetch_stats(
                selected_user,
                df
            )
        )

        st.title(
            "Top Statistics"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.header(
                "Total Messages"
            )

            st.title(
                num_messages
            )

        with col2:

            st.header(
                "Total Words"
            )

            st.title(
                words
            )

        with col3:

            st.header(
                "Media Shared"
            )

            st.title(
                num_media_messages
            )

        with col4:

            st.header(
                "Links Shared"
            )

            st.title(
                num_links
            )


        # =====================================================
        # MONTHLY TIMELINE
        # =====================================================

        st.title(
            "Monthly Timeline"
        )

        timeline = helper.monthly_timeline(
            selected_user,
            df
        )

        fig, ax = plt.subplots()

        ax.plot(

            timeline['time'],

            timeline['message'],

            color='green'

        )

        plt.xticks(
            rotation='vertical'
        )

        st.pyplot(
            fig
        )

        plt.close(
            fig
        )


        # =====================================================
        # DAILY TIMELINE
        # =====================================================

        st.title(
            "Daily Timeline"
        )

        daily_timeline = helper.daily_timeline(
            selected_user,
            df
        )

        fig, ax = plt.subplots()

        ax.plot(

            daily_timeline['only_date'],

            daily_timeline['message'],

            color='black'

        )

        plt.xticks(
            rotation='vertical'
        )

        st.pyplot(
            fig
        )

        plt.close(
            fig
        )


        # =====================================================
        # ACTIVITY MAP
        # =====================================================

        st.title(
            "Activity Map"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.header(
                "Most busy day"
            )

            busy_day = helper.week_activity_map(
                selected_user,
                df
            )

            fig, ax = plt.subplots()

            ax.bar(

                busy_day.index,

                busy_day.values,

                color='purple'

            )

            plt.xticks(
                rotation='vertical'
            )

            st.pyplot(
                fig
            )

            plt.close(
                fig
            )


        with col2:

            st.header(
                "Most busy month"
            )

            busy_month = helper.month_activity_map(
                selected_user,
                df
            )

            fig, ax = plt.subplots()

            ax.bar(

                busy_month.index,

                busy_month.values,

                color='orange'

            )

            plt.xticks(
                rotation='vertical'
            )

            st.pyplot(
                fig
            )

            plt.close(
                fig
            )


        # =====================================================
        # WEEKLY ACTIVITY MAP
        # =====================================================

        st.title(
            "Weekly Activity Map"
        )

        user_heatmap = helper.activity_heatmap(
            selected_user,
            df
        )

        if user_heatmap.empty:

            st.warning(
                "Not enough data to generate the heatmap."
            )

        else:

            fig, ax = plt.subplots()

            sns.heatmap(
                user_heatmap,
                ax=ax
            )

            st.pyplot(
                fig
            )

            plt.close(
                fig
            )


        # =====================================================
        # MOST BUSY USERS
        # =====================================================

        if selected_user == 'Overall':

            st.title(
                "Most Busy Users"
            )

            x, new_df = helper.most_busy_users(
                df
            )

            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:

                ax.bar(

                    x.index,

                    x.values,

                    color='red'

                )

                plt.xticks(
                    rotation='vertical'
                )

                st.pyplot(
                    fig
                )

                plt.close(
                    fig
                )


            with col2:

                st.dataframe(
                    new_df
                )


        # =====================================================
        # WORDCLOUD
        # =====================================================

        st.title(
            "Wordcloud"
        )

        try:

            df_wc = helper.create_wordcloud(
                selected_user,
                df
            )

            if df_wc is not None:

                fig, ax = plt.subplots(
                    figsize=(10, 5)
                )

                ax.imshow(

                    df_wc.to_array(),

                    interpolation='bilinear'

                )

                ax.axis(
                    'off'
                )

                st.pyplot(
                    fig
                )

                plt.close(
                    fig
                )

            else:

                st.info(
                    "Not enough text data to generate the Wordcloud."
                )

        except Exception as e:

            st.warning(
                f"Wordcloud could not be generated: {e}"
            )


        # =====================================================
        # MOST COMMON WORDS
        # =====================================================

        most_common_df = helper.most_common_words(
            selected_user,
            df
        )

        st.title(
            "Most Common Words"
        )

        if most_common_df.empty:

            st.info(
                "Not enough text data to find common words."
            )

        else:

            fig, ax = plt.subplots()

            ax.barh(

                most_common_df['word'],

                most_common_df['count']

            )

            plt.xticks(
                rotation='vertical'
            )

            st.pyplot(
                fig
            )

            plt.close(
                fig
            )


        # =====================================================
        # EMOJI ANALYSIS
        # =====================================================

        emoji_df = helper.emoji_helper(
            selected_user,
            df
        )

        st.title(
            "Emoji Analysis"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.dataframe(
                emoji_df
            )

        with col2:

            if emoji_df.empty:

                st.info(
                    "No emojis found in the selected chat."
                )

            else:

                fig, ax = plt.subplots()

                ax.pie(

                    emoji_df['count'].head(),

                    labels=emoji_df['emoji'].head(),

                    autopct="%0.2f"

                )

                st.pyplot(
                    fig
                )

                plt.close(
                    fig
                )


    # =========================================================
    # =========================================================
    #              REPLY PREDICTION
    # =========================================================
    #
    # IMPORTANT:
    # THIS IS OUTSIDE show_analysis.
    #
    # Therefore clicking "Predict Reply" will NOT make
    # this section disappear.
    # =========================================================


    st.divider()

    st.title(
        "🔮 Reply Prediction"
    )

    st.write(
        "Predict whether a message is likely to receive "
        "a reply, who may reply first, and the expected "
        "response time."
    )


    # =====================================================
    # AVAILABLE USERS FOR PREDICTION
    # =====================================================

    prediction_users = [

        user

        for user in df['user'].unique()

        if user != 'group_notification'

    ]


    # =====================================================
    # CHECK USERS
    # =====================================================

    if len(prediction_users) < 2:

        st.warning(
            "Reply prediction requires at least "
            "two users in the conversation."
        )

    else:

        # =================================================
        # CREATE REPLY DATASET
        # =================================================

        with st.spinner(
            "Preparing conversation data..."
        ):

            reply_df = helper.create_reply_dataset(
                df,
                response_window=60
            )


        # =================================================
        # CHECK DATA
        # =================================================

        if reply_df.empty:

            st.warning(
                "No usable conversation data was found "
                "for reply prediction."
            )

        else:

            total_turns = len(
                reply_df
            )

            replied_turns = int(
                reply_df['got_reply'].sum()
            )

            reply_rate = (

                replied_turns
                / total_turns

            ) * 100


            # =================================================
            # TRAINING INFORMATION
            # =================================================

            st.caption(

                f"Training samples: {total_turns} | "
                f"Messages with replies: {replied_turns} | "
                f"Historical reply rate: "
                f"{reply_rate:.1f}%"

            )


            # =================================================
            # TRAIN MODEL
            # =================================================

            if total_turns < 30:

                st.warning(

                    "There are not enough conversation "
                    "samples to train the reply prediction model. "
                    "Try using a larger WhatsApp chat export."

                )

            else:

                with st.spinner(
                    "Training reply prediction models..."
                ):

                    models = helper.train_reply_models(
                        reply_df
                    )


                if models is None:

                    st.error(
                        "The reply prediction model "
                        "could not be trained."
                    )

                else:

                    # =================================================
                    # INPUT SECTION
                    # =================================================

                    st.subheader(
                        "💬 Test a New Message"
                    )


                    # =================================================
                    # FORM
                    # =================================================

                    with st.form(
                        "reply_prediction_form"
                    ):

                        # ---------------------------------------------
                        # WHO IS SENDING?
                        # ---------------------------------------------

                        sender = st.selectbox(

                            "Who is sending the message?",

                            prediction_users

                        )


                        # ---------------------------------------------
                        # MESSAGE
                        # ---------------------------------------------

                        message = st.text_area(

                            "Enter your message",

                            placeholder=(
                                "Example: "
                                "Guys, kal college aa rahe ho?"
                            ),

                            height=100

                        )


                        # ---------------------------------------------
                        # TIME + DAY
                        # ---------------------------------------------

                        col1, col2 = st.columns(2)


                        with col1:

                            hour = st.slider(

                                "Time",

                                min_value=0,

                                max_value=23,

                                value=18

                            )


                        with col2:

                            day = st.selectbox(

                                "Day",

                                [

                                    "Monday",

                                    "Tuesday",

                                    "Wednesday",

                                    "Thursday",

                                    "Friday",

                                    "Saturday",

                                    "Sunday"

                                ]

                            )


                        # ---------------------------------------------
                        # BUTTON
                        # ---------------------------------------------

                        predict_button = st.form_submit_button(

                            "🔮 Predict Reply"

                        )


                    # =================================================
                    # PREDICTION RESULT
                    # =================================================

                    if predict_button:

                        # ---------------------------------------------
                        # CHECK MESSAGE
                        # ---------------------------------------------

                        if not message.strip():

                            st.warning(

                                "Please enter a message first."

                            )

                        else:

                            # -----------------------------------------
                            # DAY MAPPING
                            # -----------------------------------------

                            day_mapping = {

                                "Monday": 0,

                                "Tuesday": 1,

                                "Wednesday": 2,

                                "Thursday": 3,

                                "Friday": 4,

                                "Saturday": 5,

                                "Sunday": 6

                            }


                            # -----------------------------------------
                            # RUN MODEL
                            # -----------------------------------------

                            with st.spinner(
                                "Predicting..."
                            ):

                                result = helper.predict_reply(

                                    message,

                                    sender,

                                    models,

                                    hour,

                                    day_mapping[day]

                                )


                            # -----------------------------------------
                            # SAFETY CHECK
                            # -----------------------------------------

                            if result is None:

                                st.error(
                                    "Prediction could not be generated."
                                )

                            else:

                                st.divider()


                                # =================================================
                                # RESULT 1
                                # WILL YOU GET A REPLY?
                                # =================================================

                                st.subheader(
                                    "📩 Will you get a reply?"
                                )


                                probability = result[
                                    'reply_probability'
                                ]


                                col1, col2 = st.columns(2)


                                with col1:

                                    st.metric(

                                        "Reply Probability",

                                        f"{probability:.1f}%"

                                    )


                                with col2:

                                    if probability >= 50:

                                        st.success(

                                            "Likely to receive a reply"

                                        )

                                    else:

                                        st.info(

                                            "Less likely to receive a reply"

                                        )


                                # =================================================
                                # RESULT 2
                                # WHO WILL REPLY?
                                # =================================================

                                st.subheader(
                                    "👤 Who will probably reply first?"
                                )


                                responder_probs = result[
                                    'responder_probabilities'
                                ]


                                if responder_probs:

                                    # ---------------------------------------------
                                    # SORT USERS BY PROBABILITY
                                    # ---------------------------------------------

                                    sorted_users = sorted(

                                        responder_probs.items(),

                                        key=lambda x: x[1],

                                        reverse=True

                                    )


                                    top_users = sorted_users[:5]


                                    # ---------------------------------------------
                                    # DATAFRAME
                                    # ---------------------------------------------

                                    responder_df = pd.DataFrame(

                                        top_users,

                                        columns=[

                                            "User",

                                            "Probability (%)"

                                        ]

                                    )


                                    responder_df[
                                        "Probability (%)"
                                    ] = (

                                        responder_df[
                                            "Probability (%)"
                                        ].round(2)

                                    )


                                    st.dataframe(

                                        responder_df,

                                        use_container_width=True,

                                        hide_index=True

                                    )


                                    # ---------------------------------------------
                                    # TOP RESPONDER
                                    # ---------------------------------------------

                                    first_user = top_users[0][0]

                                    first_probability = top_users[0][1]


                                    st.success(

                                        f"Most likely first responder: "
                                        f"{first_user} "
                                        f"({first_probability:.1f}%)"

                                    )


                                else:

                                    st.info(

                                        "There is not enough responder "
                                        "data to predict who will reply."

                                    )


                                # =================================================
                                # RESULT 3
                                # RESPONSE TIME
                                # =================================================

                                st.subheader(
                                    "⏱️ Expected Response Time"
                                )


                                predicted_time = result[
                                    'predicted_time'
                                ]


                                if predicted_time is not None:

                                    # ---------------------------------------------
                                    # LESS THAN 1 MINUTE
                                    # ---------------------------------------------

                                    if predicted_time < 1:

                                        st.metric(

                                            "Expected response time",

                                            "< 1 minute"

                                        )


                                    # ---------------------------------------------
                                    # LESS THAN 60 MINUTES
                                    # ---------------------------------------------

                                    elif predicted_time < 60:

                                        st.metric(

                                            "Expected response time",

                                            f"{predicted_time:.1f} minutes"

                                        )


                                    # ---------------------------------------------
                                    # HOURS
                                    # ---------------------------------------------

                                    else:

                                        hours = (

                                            predicted_time
                                            / 60

                                        )


                                        st.metric(

                                            "Expected response time",

                                            f"{hours:.1f} hours"

                                        )


                                else:

                                    st.info(

                                        "Not enough response-time "
                                        "data to make a prediction."

                                    )