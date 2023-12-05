# Generated by Django 4.2.2 on 2023-07-11 10:45

from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.state import StateApps
from django.db.models import F, Func, JSONField, TextField, Value
from django.db.models.functions import Cast

# ScheduledMessage.type for onboarding emails from zerver/models/__init__.py
WELCOME = 1


def update_for_followup_day_email_templates_rename(
    apps: StateApps, schema_editor: BaseDatabaseSchemaEditor
) -> None:
    ScheduledEmail = apps.get_model("zerver", "ScheduledEmail")

    account_registered_emails = ScheduledEmail.objects.annotate(
        as_jsonb=Cast("data", JSONField())
    ).filter(type=WELCOME, as_jsonb__template_prefix="zerver/emails/followup_day1")
    account_registered_emails.update(
        data=Cast(
            Func(
                F("as_jsonb"),
                Value(["template_prefix"]),
                Value("zerver/emails/account_registered", JSONField()),
                function="jsonb_set",
            ),
            TextField(),
        )
    )

    onboarding_zulip_topics_emails = ScheduledEmail.objects.annotate(
        as_jsonb=Cast("data", JSONField())
    ).filter(type=WELCOME, as_jsonb__template_prefix="zerver/emails/followup_day2")
    onboarding_zulip_topics_emails.update(
        data=Cast(
            Func(
                F("as_jsonb"),
                Value(["template_prefix"]),
                Value("zerver/emails/onboarding_zulip_topics", JSONField()),
                function="jsonb_set",
            ),
            TextField(),
        )
    )


def revert_followup_day_email_templates_rename(
    apps: StateApps, schema_editor: BaseDatabaseSchemaEditor
) -> None:
    ScheduledEmail = apps.get_model("zerver", "ScheduledEmail")

    rename_extradata_realmauditlog_extra_data_json = ScheduledEmail.objects.annotate(
        as_jsonb=Cast("data", JSONField())
    ).filter(type=WELCOME, as_jsonb__template_prefix="zerver/emails/account_registered")
    rename_extradata_realmauditlog_extra_data_json.update(
        data=Cast(
            Func(
                F("as_jsonb"),
                Value(["template_prefix"]),
                Value("zerver/emails/followup_day1", JSONField()),
                function="jsonb_set",
            ),
            TextField(),
        )
    )

    rename_extradata_realmauditlog_extra_data_json = ScheduledEmail.objects.annotate(
        as_jsonb=Cast("data", JSONField())
    ).filter(type=WELCOME, as_jsonb__template_prefix="zerver/emails/onboarding_zulip_topics")
    rename_extradata_realmauditlog_extra_data_json.update(
        data=Cast(
            Func(
                F("as_jsonb"),
                Value(["template_prefix"]),
                Value("zerver/emails/followup_day2", JSONField()),
                function="jsonb_set",
            ),
            TextField(),
        )
    )


class Migration(migrations.Migration):
    dependencies = [
        ("zerver", "0467_rename_extradata_realmauditlog_extra_data_json"),
    ]

    operations = [
        migrations.RunPython(
            update_for_followup_day_email_templates_rename,
            reverse_code=revert_followup_day_email_templates_rename,
        ),
    ]
