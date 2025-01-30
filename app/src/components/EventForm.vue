<template>
    <div class="event-form">
        <form>
            <div class="event-form__name mb-2">
                <label for="event-name" class="d-block fw-bolder">Event Name</label>
                <input
                    v-model="event_name"
                    type="text"
                    id="event-name"
                    name="event-name"
                    class="w-100"
                />
            </div>

            <div class="event-form__duration mb-2">
                <label for="event-duration" class="d-block fw-bolder">Event Duration</label>

                <div class="d-flex align-items-center mb-2">
                    <input
                        v-model="event_duration.hours"
                        type="number"
                        id="event-duration-hours"
                        name="event-duration-hours"
                        min="0"
                        class="me-2"
                    />
                    <label for="event-duration-hours">Hours</label>
                </div>

                <div class="d-flex align-items-center">
                    <input
                        v-model="event_duration.minutes"
                        type="number"
                        id="event-duration-minutes"
                        name="event-duration-minutes"
                        min="0"
                        class="me-2"
                    />
                    <label for="event-duration-minutes">Minutes</label>
                </div>
            </div>

            <div class="event-form__time mb-2">
                <label for="event-time" class="d-block fw-bolder">Event Time</label>
                <input v-model="event_time" type="time" id="event-time" name="event-time">
            </div>

            <div class="event-form__type mb-2">
                <label class="fw-bolder">Event Type</label>
                <div>
                    <input
                        v-model="event_type"
                        type="radio"
                        id="event-singular"
                        name="event-type"
                        value="singular"
                    >
                    <label for="event-singular">Singular Event</label>
                </div>
                <div>
                    <input
                        v-model="event_type"
                        type="radio"
                        id="event-repeat"
                        name="event-type"
                        value="repeat"
                    />
                    <label for="event-repeat">Repeat Event</label>
                </div>
            </div>

            <div class="event-form__days mb-2">
                <label class="fw-bold">
                    <span v-if="event_type === 'singular'">Event Day</span>
                    <span v-else>Event Days</span>
                </label>
                <div
                    v-for="(day, index) in days"
                    :key="index"
                    class="d-flex align-items-center me-2"
                >
                    <input
                        v-if="event_type === 'singular'"
                        v-model="event_days"
                        type="radio"
                        :id="'event-day-' + day.toLowerCase()"
                        name="event-days"
                        :value="index"
                    />
                    <input
                        v-else
                        v-model="event_days"
                        type="checkbox"
                        :id="'event-day-' + day.toLowerCase()"
                        :value="index"
                    />
                    <label :for="'event-day-' + day.toLowerCase()">{{ day }}</label>
                </div>
            </div>

            <div class="d-flex align-items-center">
                <button
                    type="submit"
                    :disabled="submit_disabled"
                    @click="submitEvent"
                    class="me-2"
                >
                    Add Event
                </button>
                <button
                    @click="$emit('cancel')"
                >
                    Cancel
                </button>
            </div>

            <p v-if="add_event_error" class="text-danger">{{ add_event_error }}</p>
        </form>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'EventForm',
    data() {
        return {
            event_name: '',
            event_duration: {
                hours: 0,
                minutes: 0,
            },
            event_time: '',
            event_type: 'singular',
            event_days: 0,
            days: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            add_event_error: null,
            event_error: false,
        }
    },
    computed: {
        submit_disabled() {
            return !this.event_name ||
                (this.event_duration.hours == 0 && this.event_duration.minutes == 0) ||
                !this.event_time ||
                (this.event_type !== 'singular' && !this.event_days.length);
        },
    },
    watch: {
        event_type(to, from) {
            if (to === 'singular') {
                this.event_days = 0;
            } else {
                this.event_days = [];
            }
        }
    },
    methods: {
        async submitEvent(event) {
            event.preventDefault();
            this.add_event_error = null;
            const days = this.event_type === 'singular' ? [this.event_days] : this.event_days;

            let data = {
                name: this.event_name,
                duration: JSON.stringify(this.event_duration),
                time: this.event_time,
                type: this.event_type,
                days: JSON.stringify(days),
            };

            try {
                await axios.post('/event/add', data);
                this.$emit('added-event');
            } catch (error) {
                if (error.status === 400) {
                    this.add_event_error = error.response.data.detail;
                } else {
                    this.add_event_error = 'An error occurred while adding the event. Please try again.';
                }
            }
        },
    }
}
</script>

<style lang="scss" scoped>
.event-form {
    input[type="checkbox"],
    input[type="radio"] {
        margin-right: 0.25rem;
    }
}
</style>
